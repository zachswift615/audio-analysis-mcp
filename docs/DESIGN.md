# Audio Analysis MCP Server - Design

## Overview

Standalone MCP server providing audio analysis tools for Claude Code. Single tool, token-efficient design.

## Project Structure

```
audio-analysis-mcp/
├── pyproject.toml
├── README.md
├── src/
│   └── audio_analysis_mcp/
│       ├── __init__.py
│       └── server.py
└── .python-version
```

## Dependencies

- `mcp` - Official MCP SDK
- `librosa` - Audio analysis
- `matplotlib` - Visualizations
- `numpy` - Numerical ops
- `scipy` - Signal processing

## Single Tool API

```
audio_analyze(path, op, [path2])
```

| Param | Type | Description |
|-------|------|-------------|
| `path` | string | Audio file path (or paths array for batch) |
| `op` | enum | Operation to perform |
| `path2` | string? | Second file for compare/diff |

### Operations

| Op | Output |
|----|--------|
| `fingerprint` | `{rms, peak, zcr, centroid, bandwidth, rolloff, duration}` |
| `formants` | `{f1, f2, f3, f4}` |
| `compare` | `{identical, max_diff, rms_diff, metrics_pct_change}` |
| `diff` | `{identical, max_diff, mean_diff}` |
| `spectrogram` | `{output_path}` |
| `waveform` | `{output_path}` |
| `waterfall` | `{output_path}` |
| `pitch` | `{f0_mean, f0_min, f0_max, output_path}` |
| `onsets` | `{count, times}` |
| `batch` | `{results: [{path, fingerprint}...]}` |

## Configuration

Output directory via env var:
- `AUDIO_ANALYSIS_OUTPUT_DIR` - defaults to `~/.audio-analysis-mcp`

Claude Code config (`.mcp.json`):
```json
{
  "mcpServers": {
    "audio-analysis": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/zachswift/projects/audio-analysis-mcp", "python", "-m", "audio_analysis_mcp.server"],
      "env": {
        "AUDIO_ANALYSIS_OUTPUT_DIR": "./audio-analysis-output"
      }
    }
  }
}
```

## Design Principles

1. **Token efficiency** - Minimal schema, terse responses
2. **Single tool** - One `audio_analyze` tool with `op` parameter
3. **File paths for images** - No inline base64, Claude reads files separately
4. **Simple errors** - Just `{"error": "message"}`
