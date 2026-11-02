# External Integrations Audit: Video-Shotcraft, Bang-Motion, Remotion-Scenes, & Pocket-TTS

**Audit Date:** 2026-10-04  
**Scope:** Video-Shotcraft (`Vincentwei1021/video-shotcraft`), Bang-Motion (`bangtutorial/bang-motion`), Remotion-Scenes (`lifeprompt-team/remotion-scenes`), and Pocket-TTS Farsi (`mehdi-hf/pocket-tts-farsi-v2` & `nimaone/persian_tts`).

---

## 1. Video-Shotcraft (`Vincentwei1021/video-shotcraft`)
- **Core Value:** Standardized catalog of **Shot Recipe Cards**. Rather than writing animation logic from scratch, each shot is treated as a recipe with distinct Entrance, Action, Camera, and Exit properties.
- **License:** Open Source / MIT.
- **Integration Decision:** Adapted directly into `motion-recipes/catalog.yaml` and `src/director/ShotPlanner.ts`.

---

## 2. Bang-Motion (`bangtutorial/bang-motion`)
- **Core Value:** Continuous Film Language ("Move like video, not slides"). Enforces continuity graphs so that the visual anchor of Scene N transforms into Scene N+1 rather than resetting the canvas.
- **License:** Open Source.
- **Integration Decision:** Adapted into `production/continuity-graph.yaml` and `VisualMotifCore.tsx`.

---

## 3. Remotion-Scenes (`lifeprompt-team/remotion-scenes`)
- **Core Value:** High-performance particle swarms, mathematical geometric morphs, and camera shake presets.
- **License:** MIT.
- **Integration Decision:** Adapted into our `motion-recipes/` library.

---

## 4. Pocket-TTS Farsi (`mehdi-hf/pocket-tts-farsi-v2` & `nimaone/persian_tts`)
- **Core Value:** Lightweight CPU-feasible ONNX Persian TTS with voice cloning capability.
- **License:** Apache-2.0 / Open Source.
- **Benchmark Evaluation:**
  - Excellent for offline local CPU synthesis.
  - However, for high-end cinematic documentary narration, Gemini 2.5 Pro TTS with natural Tehran conversational prosody exhibits superior emotional variation and contextual sentence melody.
- **Integration Decision:** Documented as offline edge engine; Gemini 2.5 Pro TTS remains the primary production target with calibrated local fallback.
