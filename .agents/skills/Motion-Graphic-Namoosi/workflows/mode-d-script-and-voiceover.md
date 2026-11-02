# WORKFLOW: MODE D — SCRIPT + VOICEOVER TO VIDEO

## Overview
Triggered when the user provides both the written script and the recorded voiceover.

### Principle of Truth Resolution
If any discrepancies occur between script and voiceover:
* **VOICEOVER = Timing Truth** (Determines frame counts, cuts, pauses, camera motion, and pacing).
* **SCRIPT = Semantic Truth** (Determines on-screen terminology, hero titles, card labels, and factual grounding). Subtitles are completely excluded.

## Step-by-Step Instructions
1. **Phonetic & Text Reconciliation**: Cross-reference the script against transcribed audio. Flag any dropped phrases or retakes.
2. **Anchor Frames to Audio**: Generate act boundaries and kinetic keyword timings directly from the audio file.
3. **Hero Titles & Key Terminology Formatting**: Use verified script spelling for on-screen typography. Voiceover subtitles are completely excluded.
4. **Construct Storyboard**: Structure camera movements around audio breathing room and emphasis.
5. **Pilot & Production**: Standard pilot validation and parallel assembly using `UniversalCinematicStoryScene.tsx`.
