# Audio Analysis MCP Tool

## When to Use

Use `mcp__audio-analysis__audio_analyze` when you need to:

- Understand audio content without listening (fingerprint, formants)
- Compare audio files before/after changes (compare, diff)
- Visually inspect frequency content (spectrogram, waterfall)
- Check for clipping, DC offset, or waveform shape (waveform)
- Track pitch over time (pitch)
- Find note onsets or transients (onsets)
- Batch analyze multiple files (batch)

## Tool Signature

```
audio_analyze(path, op, [path2])
```

- `path`: Audio file path (string, or array for batch)
- `op`: Operation - one of: `fingerprint`, `formants`, `compare`, `diff`, `spectrogram`, `waveform`, `waterfall`, `pitch`, `onsets`, `batch`
- `path2`: Second file path (only for `compare` and `diff`)

## Quick Reference

| Task | Call |
|------|------|
| Get audio stats | `{path: "out.wav", op: "fingerprint"}` |
| Estimate vowel formants | `{path: "vowel.wav", op: "formants"}` |
| Compare before/after | `{path: "before.wav", op: "compare", path2: "after.wav"}` |
| Check if identical | `{path: "a.wav", op: "diff", path2: "b.wav"}` |
| See frequency content | `{path: "out.wav", op: "spectrogram"}` |
| See waveform shape | `{path: "out.wav", op: "waveform"}` |
| 3D spectral view | `{path: "out.wav", op: "waterfall"}` |
| Track pitch/F0 | `{path: "speech.wav", op: "pitch"}` |
| Find note attacks | `{path: "melody.wav", op: "onsets"}` |
| Analyze many files | `{path: ["a.wav", "b.wav"], op: "batch"}` |

## Interpreting Results

### Fingerprint Values

- `rms`: Overall loudness (0.0-1.0 typical)
- `peak`: Max amplitude (1.0 = clipping)
- `zcr`: Zero-crossing rate - higher means more HF content or noise
- `centroid`: Spectral "brightness" in Hz - higher = brighter
- `bandwidth`: Spectral spread in Hz
- `rolloff`: Frequency below which 85% of energy lies

### Formants (vowels)

- `f1`: ~300-800 Hz, correlates with vowel height (open/close)
- `f2`: ~800-2500 Hz, correlates with front/back position
- `f3`, `f4`: Voice quality, speaker characteristics

### Visual Outputs

Spectrograms, waveforms, waterfall plots, and pitch tracks are saved to files. The tool returns `{output_path: "..."}`. Use the Read tool to view the image if needed.

## Output Directory

Images saved to `AUDIO_ANALYSIS_OUTPUT_DIR` (configured in .mcp.json), defaulting to `~/.audio-analysis-mcp`.
