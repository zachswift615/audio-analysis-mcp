#!/usr/bin/env python3
"""Audio Analysis MCP Server - Single tool, token-efficient design."""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Output directory for generated files - ensure absolute path
_output_env = os.environ.get("AUDIO_ANALYSIS_OUTPUT_DIR", "~/.audio-analysis-mcp")
OUTPUT_DIR = Path(_output_env).expanduser().resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

server = Server("audio-analysis")


def _output_path(source_path: str, op: str, ext: str = "png") -> Path:
    """Generate output path for a file."""
    stem = Path(source_path).stem
    ts = datetime.now().strftime("%H%M%S")
    return OUTPUT_DIR / f"{stem}_{op}_{ts}.{ext}"


# === Analysis Functions ===

def fingerprint(path: str) -> dict:
    """Compute numerical fingerprint of audio file."""
    y, sr = librosa.load(path, sr=None)
    return {
        "rms": round(float(np.sqrt(np.mean(y**2))), 4),
        "peak": round(float(np.max(np.abs(y))), 4),
        "zcr": round(float(np.mean(librosa.feature.zero_crossing_rate(y))), 4),
        "centroid": round(float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))), 1),
        "bandwidth": round(float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))), 1),
        "rolloff": round(float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))), 1),
        "duration": round(len(y) / sr, 3),
    }


def formants(path: str) -> dict:
    """Approximate formant analysis using LPC."""
    y, sr = librosa.load(path, sr=None)
    y_pre = librosa.effects.preemphasis(y)

    order = 10  # 2 + 4 formants * 2
    frame_len = min(2048, len(y_pre))
    mid = len(y_pre) // 2
    frame = y_pre[mid:mid + frame_len] * np.hamming(frame_len)

    # Autocorrelation + Levinson-Durbin
    r = np.correlate(frame, frame, mode='full')[len(frame)-1:]
    a = np.zeros(order + 1)
    a[0] = 1.0
    e = r[0]

    for i in range(1, order + 1):
        lam = sum(a[j] * r[i - j] for j in range(i))
        a[i] = -lam / e if e != 0 else 0
        for j in range(1, i):
            a[j] = a[j] + a[i] * a[i - j]
        e = e * (1 - a[i]**2) if abs(a[i]) < 1 else e

    roots = np.roots(a)
    roots = roots[np.imag(roots) >= 0]
    roots = roots[np.abs(roots) < 1]

    angles = np.angle(roots)
    freqs = sorted(f for f in (angles * sr / (2 * np.pi)) if f > 50)[:4]

    result = {}
    for i, f in enumerate(freqs, 1):
        result[f"f{i}"] = round(f, 1)
    return result


def compare(path1: str, path2: str) -> dict:
    """Compare two audio files."""
    fp1 = fingerprint(path1)
    fp2 = fingerprint(path2)

    y1, sr1 = librosa.load(path1, sr=None)
    y2, sr2 = librosa.load(path2, sr=None)

    # Resample if needed (resample y2 to match y1's rate)
    if sr1 != sr2:
        y2 = librosa.resample(y2, orig_sr=sr2, target_sr=sr1)

    # Pad to match lengths
    max_len = max(len(y1), len(y2))
    y1 = np.pad(y1, (0, max_len - len(y1)))
    y2 = np.pad(y2, (0, max_len - len(y2)))

    d = y2 - y1
    identical = bool(np.allclose(y1, y2, atol=1e-10))

    # Percent changes for key metrics
    pct = {}
    for k in ["rms", "centroid", "bandwidth"]:
        if fp1[k] != 0:
            pct[k] = round((fp2[k] - fp1[k]) / fp1[k] * 100, 1)

    return {
        "identical": identical,
        "max_diff": round(float(np.max(np.abs(d))), 4),
        "rms_diff": round(float(np.sqrt(np.mean(d**2))), 4),
        "pct_change": pct,
    }


def diff(path1: str, path2: str) -> dict:
    """Sample-level diff between two files."""
    y1, sr1 = librosa.load(path1, sr=None)
    y2, sr2 = librosa.load(path2, sr=None)

    # Resample if needed (resample y2 to match y1's rate)
    if sr1 != sr2:
        y2 = librosa.resample(y2, orig_sr=sr2, target_sr=sr1)

    max_len = max(len(y1), len(y2))
    y1 = np.pad(y1, (0, max_len - len(y1)))
    y2 = np.pad(y2, (0, max_len - len(y2)))

    d = y2 - y1
    return {
        "identical": bool(np.allclose(y1, y2, atol=1e-10)),
        "max_diff": round(float(np.max(np.abs(d))), 4),
        "mean_diff": round(float(np.mean(np.abs(d))), 4),
    }


def save_spectrogram(path: str) -> dict:
    """Generate and save mel spectrogram."""
    y, sr = librosa.load(path, sr=None)
    S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr), ref=np.max)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()

    out = _output_path(path, "spectrogram")
    plt.savefig(out, dpi=150)
    plt.close()

    return {"output_path": str(out)}


def save_waveform(path: str) -> dict:
    """Generate and save waveform plot."""
    y, sr = librosa.load(path, sr=None)

    plt.figure(figsize=(10, 3))
    librosa.display.waveshow(y, sr=sr)
    plt.tight_layout()

    out = _output_path(path, "waveform")
    plt.savefig(out, dpi=150)
    plt.close()

    return {"output_path": str(out)}


def save_waterfall(path: str) -> dict:
    """Generate 3D waterfall spectrogram."""
    y, sr = librosa.load(path, sr=None)

    # Compute STFT
    D = np.abs(librosa.stft(y))
    D_db = librosa.amplitude_to_db(D, ref=np.max)

    # Subsample for visualization
    hop = max(1, D_db.shape[1] // 100)
    D_sub = D_db[:, ::hop]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    freqs = librosa.fft_frequencies(sr=sr)
    times = np.arange(D_sub.shape[1])

    # Create mesh
    T, F = np.meshgrid(times, np.arange(len(freqs)))

    # Plot surface
    ax.plot_surface(T, F, D_sub, cmap='viridis', linewidth=0, antialiased=True)
    ax.set_xlabel('Time')
    ax.set_ylabel('Frequency bin')
    ax.set_zlabel('dB')
    ax.view_init(elev=30, azim=45)

    out = _output_path(path, "waterfall")
    plt.savefig(out, dpi=150)
    plt.close()

    return {"output_path": str(out)}


def pitch_track(path: str) -> dict:
    """Track pitch (F0) over time using pyin."""
    y, sr = librosa.load(path, sr=None)

    f0, voiced_flag, voiced_probs = librosa.pyin(
        y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7')
    )

    # Filter to voiced segments
    f0_voiced = f0[~np.isnan(f0)]

    if len(f0_voiced) == 0:
        return {"error": "no pitched content detected"}

    # Plot
    plt.figure(figsize=(10, 4))
    times = librosa.times_like(f0, sr=sr)
    plt.plot(times, f0, label='F0', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()

    out = _output_path(path, "pitch")
    plt.savefig(out, dpi=150)
    plt.close()

    return {
        "f0_mean": round(float(np.nanmean(f0)), 1),
        "f0_min": round(float(np.nanmin(f0_voiced)), 1),
        "f0_max": round(float(np.nanmax(f0_voiced)), 1),
        "output_path": str(out),
    }


def detect_onsets(path: str) -> dict:
    """Detect onsets/transients in audio."""
    y, sr = librosa.load(path, sr=None)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    return {
        "count": len(onset_times),
        "times": [round(t, 3) for t in onset_times.tolist()],
    }


def batch_analyze(paths: list) -> dict:
    """Batch fingerprint multiple files."""
    results = []
    for p in paths:
        try:
            results.append({"path": p, "fingerprint": fingerprint(p)})
        except Exception as e:
            results.append({"path": p, "error": str(e)})
    return {"results": results}


# === MCP Tool Registration ===

OPERATIONS = {
    "fingerprint": lambda p, p2: fingerprint(p),
    "formants": lambda p, p2: formants(p),
    "compare": lambda p, p2: compare(p, p2),
    "diff": lambda p, p2: diff(p, p2),
    "spectrogram": lambda p, p2: save_spectrogram(p),
    "waveform": lambda p, p2: save_waveform(p),
    "waterfall": lambda p, p2: save_waterfall(p),
    "pitch": lambda p, p2: pitch_track(p),
    "onsets": lambda p, p2: detect_onsets(p),
    "batch": lambda p, p2: batch_analyze(p if isinstance(p, list) else [p]),
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="audio_analyze",
            description="Analyze audio. ops: fingerprint|formants|compare|diff|spectrogram|waveform|waterfall|pitch|onsets|batch",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": ["string", "array"],
                        "description": "Audio file path (or array for batch)",
                    },
                    "op": {
                        "type": "string",
                        "enum": list(OPERATIONS.keys()),
                        "description": "Operation to perform",
                    },
                    "path2": {
                        "type": "string",
                        "description": "Second file for compare/diff",
                    },
                },
                "required": ["path", "op"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name != "audio_analyze":
        return [TextContent(type="text", text=json.dumps({"error": f"unknown tool: {name}"}))]

    path = arguments.get("path")
    op = arguments.get("op")
    path2 = arguments.get("path2")

    if op not in OPERATIONS:
        return [TextContent(type="text", text=json.dumps({"error": f"unknown op: {op}"}))]

    try:
        result = OPERATIONS[op](path, path2)
        return [TextContent(type="text", text=json.dumps(result))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
