---
description: Compare synthesized audio against reference, track improvements across versions
argument-hint: <reference.wav> <synthesized.wav> [version-context]
allowed-tools: Skill(analyze-audio-iterations), mcp__audio-analysis__audio_analyze, Read
---

<objective>
Delegate audio comparison to the analyze-audio-iterations skill for: $ARGUMENTS

This routes to specialized skill containing analysis workflows, metrics interpretation, and version tracking patterns.
</objective>

<process>
1. Use Skill tool to invoke analyze-audio-iterations skill
2. Pass user's audio files and version context: $ARGUMENTS
3. Let skill handle comprehensive analysis workflow
</process>

<success_criteria>
- Skill successfully invoked
- All audio analyses run in parallel
- Visual outputs inspected
- Metrics tables generated
- Recommendations provided
</success_criteria>
