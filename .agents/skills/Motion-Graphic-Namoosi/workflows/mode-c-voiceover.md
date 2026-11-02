# WORKFLOW: MODE C — VOICEOVER TO VIDEO

## Overview
Triggered when the user provides pre-recorded voiceover audio files.

> [!IMPORTANT]
> The audio recording is the single source of timing truth. Video frames, camera cuts, and kinetic emphasis tokens must anchor strictly to audio timestamps. Voiceover subtitles are completely banned.

```text
AUDIO FILE (.wav / .mp3)
    ↓
TRANSCRIPTION & BEAT BOUNDARIES
    ↓
FRAME-ACCURATE TIMELINE (Acts & Climax Keywords)
    ↓
BEAT SHEET & STORYBOARD (Zero Subtitle Displays)
    ↓
PILOT GATE (First 20s)
    ↓
FULL BUILD & RENDER
```

## Step-by-Step Instructions
1. **Import Audio**: Place audio in `public/assets/<slug>/audio.wav`.
2. **Extract Word-Level Timestamps**: Use audio analysis to locate semantic sentence boundaries and climax keywords.
3. **Map Semantic Act Beats to Audio Peaks**: Register exact start and end frames for narrative acts and keyword emphasis points. Do NOT generate or render voiceover subtitles.
4. **Draft Visual Beats to Match Audio Peaks**: Align visual impacts to precede voiceover emphasis points by 2–3 frames.
5. **Pilot & Parallel Build**: Standard execution using `UniversalCinematicStoryScene.tsx` and locked design tokens.
