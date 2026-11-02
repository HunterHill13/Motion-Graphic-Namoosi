# WORKFLOW: MODE B — SCRIPT TO VIDEO

## Overview
Triggered when the user provides an existing written script or narration text.

> [!IMPORTANT]
> The user's script is immutable semantic truth. Never rewrite, summarize, or alter core technical terms without explicit permission.

```text
USER SCRIPT
    ↓
GATE 0.1: VOICE SELECTION (Puck / Callirrhoe)
    ↓
GATE 0.5: COLOR PALETTE SELECTION
    ↓
GATE 0.8: SCRIPT ACT SEGMENTATION (2 to 6 Narrative Acts)
    ↓
STAGE 1 AUDIO: EDGE-TTS PREVIEW (Zero Gemini Quota)
    ↓
PILOT PREVIEW RENDER & USER SIGN-OFF
    ↓ (USER APPROVAL)
STAGE 2 AUDIO: MASTER GEMINI AUDIO (cinematic_audio_pipeline.py)
    ↓
CANONICAL STUDIO SCENE BUILD (UniversalCinematicStoryScene.tsx)
    ↓
QC AUDIT & FINAL MP4 DELIVERY
```

## Step-by-Step Instructions

1. **Analyze User Script & Genre**:
   - Parse sentence breaks, technical keywords, and tone.
   - Align script into 2 to 6 dramatic acts matching the organic genre (Keynote, Scientific, Manifesto, or Tactile).
   - Identify 1-2 kinetic emphasis keywords per act for `KineticEmphasisCallout`.

2. **Select Voice & Visual Palette**:
   - Execute Gate 0.1 (Puck / Callirrhoe) and Gate 0.5 (3 topic palettes) via `ask_question`.

3. **Stage 1 Audio Preview**:
   - Synthesize preview with Edge-TTS to measure cadence and timing without consuming Gemini quota.
   - Wire up preliminary Remotion composition based on `UniversalCinematicStoryScene.tsx`.

4. **Stage 2 Master Audio**:
   - Run `python scripts/cinematic_audio_pipeline.py` to generate master Gemini voiceover.
   - Strip tail buffer overrun with `strip_gemini_trailing_artifact`.
   - Lock composition frame length to master audio.

5. **Inviolable Cinematic Wiring (Gate 0.8)**:
   - Build composition with `PersistentWorld` and `UniversalCameraRig`.
   - Distribute acts across discrete 3D spatial stations ($x_1=0, x_2=1400, \dots$ or deep Z).
   - Incorporate `LottieGraphic` vectors and `KineticEmphasisCallout` typography tokens.
   - Enforce Gate 0.7 Hard Legibility Floors (never render body text below 32px or hero heads below 92px).

6. **QC Audit & Delivery**:
   - Validate TypeScript types (`npx tsc --noEmit`).
   - Render final high-definition MP4.
