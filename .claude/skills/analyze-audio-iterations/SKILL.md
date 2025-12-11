---
name: analyze-audio-iterations
description: Compare synthesized audio against recorded reference to identify quantifiable differences and track improvement across versions. Use when comparing audio files, analyzing synthesis quality, or iterating on audio generation with version tracking.
---

<objective>
Provide comprehensive audio analysis comparing synthesized audio against a recorded reference, tracking metrics across multiple versions to identify improvements, regressions, and actionable next steps.
</objective>

<quick_start>
<single_comparison>
Run all analyses in parallel for comprehensive comparison:

```
mcp__audio-analysis__audio_analyze (compare): reference + synthesized
mcp__audio-analysis__audio_analyze (diff): reference + synthesized
mcp__audio-analysis__audio_analyze (spectrogram): reference
mcp__audio-analysis__audio_analyze (spectrogram): synthesized
mcp__audio-analysis__audio_analyze (fingerprint): reference
mcp__audio-analysis__audio_analyze (fingerprint): synthesized
mcp__audio-analysis__audio_analyze (formants): reference
mcp__audio-analysis__audio_analyze (formants): synthesized
mcp__audio-analysis__audio_analyze (onsets): reference
mcp__audio-analysis__audio_analyze (onsets): synthesized
mcp__audio-analysis__audio_analyze (waterfall): reference
mcp__audio-analysis__audio_analyze (waterfall): synthesized
```

Then read spectrogram and waterfall images with the Read tool to analyze visually.
</single_comparison>

<version_tracking>
When analyzing version N, maintain running comparison tables showing all versions (v5, v6, v7...) to reveal trends - what's improving, what's oscillating, what's stuck.
</version_tracking>
</quick_start>

<workflow>
<step_1>
**Run parallel analyses**: Execute all audio analysis operations in a single parallel batch. Use `compare` and `diff` ops with both files, individual ops (spectrogram, fingerprint, formants, onsets, waterfall) for each file separately.
</step_1>

<step_2>
**View visual outputs**: Read spectrogram and waterfall PNG files to analyze spectral shape, energy distribution, temporal variation, and frequency content visually.
</step_2>

<step_3>
**Build metrics tables**: Compile quantitative data into comparison tables:

| Feature | Recorded | Synthesized | Error |
|---------|----------|-------------|-------|
| RMS | X | Y | +/-% |
| Spectral Centroid | X Hz | Y Hz | +/-% |
| Bandwidth | X Hz | Y Hz | +/-% |
| Rolloff (85%) | X Hz | Y Hz | +/-% |
| Zero-Crossing Rate | X | Y | +/-% |
| Peak | X | Y | +/-% |
| Peak/RMS ratio | X | Y | +/-% |
| Onset count | X | Y | - |
</step_3>

<step_4>
**Analyze percentage changes** from the compare operation:
- `pct_change.rms`: Overall loudness difference
- `pct_change.centroid`: Spectral brightness/darkness
- `pct_change.bandwidth`: Spectral spread
</step_4>

<step_5>
**Interpret formants**: Compare formant frequencies (F1, F2, F3, F4). For fricatives, higher formants indicate more high-frequency energy. Values at Nyquist (22050 Hz) indicate energy extending to the frequency limit.
</step_5>

<step_6>
**Assess micro-modulation**: Compare onset counts. Natural recordings typically have more detected onsets due to subtle amplitude variation. Low onset counts suggest overly steady/synthetic character.
</step_6>

<step_7>
**Provide recommendations**: Based on deltas, specify concrete adjustments:
- Centroid too low → increase high-frequency energy
- RMS wrong → adjust gain
- Bandwidth off → adjust filter Q/spread
- Missing onsets → add amplitude modulation
</step_7>
</workflow>

<multi_version_tracking>
<evolution_table>
When tracking multiple versions, maintain a running table:

| Metric | v5 | v6 | v7 | v8 | Target | Status |
|--------|----|----|----|----|--------|--------|
| RMS | -25% | +8% | +115% | +0.5% | 0% | FIXED |
| Centroid | -15% | -1% | +3% | -15% | 0% | REGRESSED |

Use status indicators:
- **FIXED**: Within 5% of target
- **IMPROVED**: Moving toward target
- **REGRESSED**: Moving away from target
- **OSCILLATING**: Bouncing back and forth
</evolution_table>

<pattern_detection>
Watch for common patterns:
- **Amplitude/spectrum trade-off**: Fixing amplitude breaks spectrum (or vice versa)
- **Overcorrection**: Each version overshoots in opposite direction
- **Plateau**: Metric stuck despite changes

When patterns detected, note them explicitly and suggest breaking the cycle.
</pattern_detection>
</multi_version_tracking>

<key_metrics>
<primary_metrics>
These metrics have the biggest perceptual impact:

- **Spectral Centroid**: Perceived brightness. Most important for fricative character.
- **RMS Level**: Overall loudness. Easy to match but often traded against spectrum.
- **Rolloff Frequency**: Where high-frequency energy drops off. Affects "airiness".
- **Bandwidth**: Spectral spread. Too wide = thin, too narrow = focused.
</primary_metrics>

<secondary_metrics>
- **Zero-Crossing Rate**: Correlates with high-frequency content
- **Peak/RMS Ratio**: Dynamic character (spiky vs dense)
- **Onset Count**: Temporal variation/naturalness
- **Formants**: Resonance structure (for voiced sounds)
</secondary_metrics>
</key_metrics>

<visual_analysis>
<spectrogram_checklist>
When viewing spectrograms, check:

- [ ] Highpass behavior below 500 Hz (should be attenuated for fricatives)
- [ ] Peak energy band location (typically 4-8 kHz for /s/)
- [ ] High-frequency extension (energy up to 16 kHz+)
- [ ] Temporal uniformity (natural has subtle variation)
- [ ] Overall brightness compared to reference
</spectrogram_checklist>

<waterfall_checklist>
When viewing waterfall plots, check:

- [ ] Spectral envelope shape (rise-to-peak-then-rolloff vs flat)
- [ ] Peak height relative to low/high frequencies
- [ ] Consistency across time slices
</waterfall_checklist>
</visual_analysis>

<sound_type_guidance>
<fricatives>
Key characteristics:
- Broadband noise with spectral shaping
- Spectral centroid typically 4-8 kHz (/s/, /z/) or lower (/f/, /v/, /th/)
- Highpass below ~300-500 Hz (no vocal tract resonance leakage)
- Spectral slope follows turbulence physics (Kolmogorov -5/3 for fully developed)

Common issues:
- Too narrow bandwidth (sounds "whistly")
- Missing high-frequency extension (sounds "dull")
- Low-frequency rumble (sounds "breathy")
- Too uniform temporally (sounds "synthetic")
</fricatives>

<other_sounds>
Extend this section with guidance for:
- Plosives (burst characteristics, VOT)
- Vowels (formant matching, harmonics)
- Sibilants (vs non-sibilant fricatives)
</other_sounds>
</sound_type_guidance>

<report_template>
<single_version_report>
## Comparison: [Reference] vs [Synthesized vN]

### Direct Comparison Metrics
| Metric | Value |
|--------|-------|
| Max Difference | X |
| RMS Difference | X |
| Mean Difference | X |

### Percentage Changes (Synthesized relative to Recorded)
| Metric | Change |
|--------|--------|
| RMS Level | +/-X% |
| Spectral Centroid | +/-X% |
| Bandwidth | +/-X% |

### Fingerprint Comparison
[Full metrics table]

### Formant Analysis
[Formant comparison table]

### Visual Spectrogram Analysis
[Observations from spectrogram/waterfall]

### Recommendations for Next Version
1. [Specific adjustment]
2. [Specific adjustment]
</single_version_report>

<multi_version_report>
## Evolution Summary: v5 → v6 → v7 → vN

### Progress Table
[Full evolution table with status indicators]

### What's Working
- [Metric]: [Status and value]

### What Needs Attention
- [Metric]: [Issue and recommendation]

### Detected Patterns
- [Pattern name]: [Description and suggested fix]

### Recommendations for vN+1
[Prioritized list combining best of previous versions]
</multi_version_report>
</report_template>

<success_criteria>
A successful analysis includes:

- All 7 analysis types run (compare, diff, spectrogram, fingerprint, formants, onsets, waterfall)
- Visual inspection of spectrogram and waterfall images
- Quantitative metrics compiled into comparison tables
- Percentage errors calculated for all key metrics
- For multi-version: evolution table with trend indicators
- Specific, actionable recommendations for next iteration
- Pattern detection when oscillation or trade-offs observed
</success_criteria>
