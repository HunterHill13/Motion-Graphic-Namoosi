# WORKFLOW: MODE A — TOPIC TO VIDEO

## Overview
Triggered when the user provides an open topic, idea, or concept (e.g. *"یک ویدیو در مورد CRISPR یا سیستم‌های توزیع‌شده بساز"*).

```text
TOPIC & REQUIREMENTS
        ↓
GATE 0.1: VOICE SELECTION (Puck / Callirrhoe)
        ↓
GATE 0.5: COLOR PALETTE SELECTION (3 Chromatic Options)
        ↓
GATE 0.8: GENRE-DRIVEN SCENARIO ADAPTATION (Keynote, Scientific, Manifesto, or Tactile)
        ↓
STAGE 1 AUDIO: EDGE-TTS PREVIEW (Zero Gemini Quota)
        ↓
PREVIEW VIDEO RENDER & USER APPROVAL (Pacing, Motion, Typography)
        ↓ (USER APPROVAL)
STAGE 2 AUDIO: GEMINI TTS + SURGICAL OVERRUN PURGE (cinematic_audio_pipeline.py)
        ↓
CANONICAL STUDIO BUILD (UniversalCinematicStoryScene.tsx)
        ↓ (UniversalCameraRig + Multi-Act 3D Stations + KineticEmphasisCallout + Lottie)
TWO-TIER QC & FINAL DELIVERY
```

## Step-by-Step Instructions

1. **Gate 0.1 & Gate 0.5 - Voice & Chromatic DNA**:
   - Ask user to select voice (Puck / Callirrhoe) via `ask_question`.
   - Propose 3 topic-tailored palettes plus custom write-in.

2. **Gate 0.8 - Dynamic Genre-Driven Scenario Writing**:
   - Classify topic into one of 4 narrative genres (do NOT force a rigid cookie-cutter structure):
     * *Keynote Launch*: Challenge -> Innovation Engine -> 10x Climax -> Future Ecosystem.
     * *Scientific Explainer*: Curiosity Hook -> Deep Mechanism -> Empirical Proof -> Paradigm Shift.
     * *Brand Manifesto*: Philosophical Contrast -> Structural Monolith -> Kinetic Words -> Vision.
     * *Tactile Narrative*: Real-world Problem -> Intuitive Metaphor -> Step-by-step Resolve -> Takeaway.
   - For every act (2 to 6 acts), define: Dramatic Goal, Hero Visual Entity, Discrete 3D Coordinates (e.g. x=0, 1400, 2800), 1-2 Kinetic Emphasis Tokens, and Lottie Preset.

3. **Stage 1 Audio - Zero-Quota Motion Preview**:
   - Synthesize preview narration via Edge-TTS (`fa-IR-FaridNeural` / `DilaraNeural`).
   - Extract beat boundaries and render fast preview for user sign-off.

4. **Stage 2 Audio - Master Gemini Narration**:
   - Upon user approval, run `python scripts/cinematic_audio_pipeline.py` to synthesize master audio.
   - Enforce trailing buffer overrun purge (`strip_gemini_trailing_artifact`) for zero-noise tail.
   - Recalibrate composition frames to exact measured Gemini audio duration.

5. **Canonical Composition Construction (MANDATORY)**:
   - Base code strictly on `src/motion/templates/UniversalCinematicStoryScene.tsx`.
   - Wire `PersistentWorld` and `UniversalCameraRig` across all acts. Static flat `<div>` containers are strictly rejected as **Unmotivated Slideshow Defects**.
   - Enforce Gate 0.7 Hard Legibility Floors (`LEGIBILITY_FLOORS_16_9`) and safe zone occupation (65%-80% width in 16:9).
   - Integrate `KineticEmphasisCallout` and `LottieGraphic` in every act.

6. **QC & Verification**:
   - Run `npx tsc --noEmit` and Remotion frame render checks.
   - Deliver final MP4 with delivery notes.
