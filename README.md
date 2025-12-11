# Audio Analysis MCP Server

An MCP server that gives Claude Code the ability to analyze audio files without ears. Provides numerical fingerprints, visual spectrograms, pitch tracking, and more - all through a single, token-efficient tool.

## Overview

This server exposes one tool (`audio_analyze`) with multiple operations, keeping the MCP schema small and token usage minimal. Visual outputs (spectrograms, waveforms, etc.) are saved to disk and paths returned - Claude can then read the images separately if needed.

## Installation

```bash
cd ~/projects/audio-analysis-mcp
~/.local/bin/uv sync
```

If you don't have `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Configuration

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "audio-analysis": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/audio-analysis-mcp",
        "python",
        "-m",
        "audio_analysis_mcp.server"
      ],
      "env": {
        "AUDIO_ANALYSIS_OUTPUT_DIR": "./audio-analysis-output"
      }
    }
  }
}
```

Or add to `~/.claude.json` to make it available globally.

## Operations

Single tool: `audio_analyze(path, op, [path2])`

### Numerical Analysis

| Op | Description | Output |
|----|-------------|--------|
| `fingerprint` | RMS, peak, spectral stats | `{rms, peak, zcr, centroid, bandwidth, rolloff, duration}` |
| `formants` | Estimated F1-F4 frequencies | `{f1, f2, f3, f4}` |
| `compare` | Compare two files numerically | `{identical, max_diff, rms_diff, pct_change}` |
| `diff` | Sample-level difference | `{identical, max_diff, mean_diff}` |
| `onsets` | Detect transients/attacks | `{count, times}` |
| `batch` | Fingerprint multiple files | `{results: [...]}` |

### Visual Analysis

| Op | Description | Output |
|----|-------------|--------|
| `spectrogram` | Mel spectrogram image | `{output_path}` |
| `waveform` | Amplitude over time | `{output_path}` |
| `waterfall` | 3D spectral surface | `{output_path}` |
| `pitch` | F0 tracking plot + stats | `{f0_mean, f0_min, f0_max, output_path}` |

## Output Directory

Images are saved to the directory specified by `AUDIO_ANALYSIS_OUTPUT_DIR` env var. Defaults to `~/.audio-analysis-mcp` if not set.

## Claude Code Skill & Slash Command

This project includes a Claude Code skill and slash command for structured audio comparison workflows.

### Installing the Skill

Copy the skill to your Claude Code skills directory:

```bash
cp -r .claude/skills/analyze-audio-iterations ~/.claude/skills/
```

This enables automatic detection when you're comparing audio files, with structured workflows for:
- Running all 7 analysis types in parallel
- Building metrics comparison tables
- Tracking improvements across versions
- Pattern detection (oscillation, trade-offs, plateaus)

### Installing the Slash Command

Copy the slash command to your Claude Code commands directory:

```bash
cp .claude/commands/analyze-audio.md ~/.claude/commands/
```

Then use it with:

```
/analyze-audio /path/to/reference.wav /path/to/synthesized.wav [version-context]
```

### Quick Install (Both)

```bash
cp -r .claude/skills/analyze-audio-iterations ~/.claude/skills/ && \
cp .claude/commands/analyze-audio.md ~/.claude/commands/
```

## Dependencies

- `mcp` - Official MCP Python SDK
- `librosa` - Audio analysis
- `matplotlib` - Visualizations
- `numpy`, `scipy` - Numerical operations
