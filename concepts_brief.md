# Motion Graphic Director: General Topic Synthesis & Architecture Overhaul

* **Author:** Motion Director Architecture Team
* **Date:** 2026-11-01

## Overview

The user questioned two core capabilities of the system:
1. Whether the Motion Director AI agent can autonomously design storyboards and synchronized procedural sound effects for *any* arbitrary input topic at the benchmark quality level.
2. Whether the motion graphics skill and agent instructions have genuinely transitioned away from the legacy, failed Remotion slide-deck strategy.

This brief evaluates the feasibility, system boundaries, and architectural fixes applied to resolve the legacy debt.

## Critical Analysis & Risk Assessment

### 1. Can the agent autonomously storyboard and design SFX for *any* arbitrary topic?

**Stress-Test Finding: NOT unconditionally without strict constraints.**

While the mathematical engine (`render.mjs`, `mgaudio`, Canvas 2D/SVG physics) is fully operational on Windows, the LLM directing pipeline faces three critical bottlenecks when given an unconstrained, arbitrary topic:

* **The Semantic Metaphor Trap (Slide-Deck Bias):**
  When given open topics (e.g., "Medical AI", "Fintech"), default LLM behavior generates expository paragraphs, title cards, and floating text boxes. Real motion design (as proven by the `01-flat-vector` and `08-morph` benchmarks) operates on pure visual metaphor (e.g., a single dot traversing a kinetic machine, or a polygon morphing through 8 distinct tool forms). Typography is strictly restricted to 1–3 monumental punch words. If an incoming topic cannot be distilled into a geometric metaphor, the output degrades into animated slides.

* **Procedural Canvas/SVG Generation Limits:**
  Generating 300–600 lines of bug-free, continuous Canvas 2D or SVG vector drawing math for complex, non-trivial objects (e.g., anatomical organs, intricate mechanical rigs) in a single shot has a failure rate. The benchmark works because the geometries are disciplined (clean geometric shapes, 240-vertex sampled polygon loops, SVG path matrices).

* **Audio-Visual Tight Coupling (`cues.json`):**
  The procedural audio engine (`mgaudio`) does not use pre-recorded background tracks. It synthesizes music and SFX via Python code mapped directly to exact frame numbers in `cues.json`. If the visual cues shift or lack explicit physical momentum (launch, impact, snap, wipe), the audio script produces disconnected or arrhythmic sound design.

### 2. Was the system still trapped in the legacy architecture?

**Stress-Test Finding: YES, until this audit.**

The user's skepticism was completely justified by codebase inspection:
* The local workspace files (`AGENTS.md`, `.agents/skills/...`) were updated, **BUT** the global Antigravity/Gemini plugin files at `C:\Users\Hill\.gemini\config\plugins\motion-director/` remained completely unaltered.
* Specifically:
  - `agents/motion-director.md` was still mandating Remotion components in `src/motion/` and `SpringPhysicsMatrix.ts`.
  - `agents/motion-director-auditor.md` still contained legacy Remotion checks (e.g., "banning 2D flat icons" and enforcing "Zero-SFX / no foley").
  - `skills/cinematic-motion-director/SKILL.md` still contained obsolete Remotion templates and prohibited procedural SFX.
* **Resolution Applied:** All three global plugin files have now been directly overwritten to mirror the 15 canonical styles, `cues.json` master frame sheet, procedural `mgaudio` DSP, and headless Chrome rendering harness.

## Goals vs. Non-Goals

* **In-Scope Goals:**
  - Enforce the 4-beat cinematic structure (0.0–0.5s Hook, 0.5–6.0s Escalation, 6.0–8.0s Hero Peak, 8.0–10.0s Living Hold) for any proposed topic.
  - Require every topic to define a single primary geometric metaphor before authoring code.
  - Couple every visual event to a micro-second hit in `cues.json` and a synthesized sound event in `audio.py`.
  - Maintain 100% local headless Chrome GPU rendering (0.02s–0.4s per frame).

* **Out-of-Scope Non-Goals:**
  - Supporting slide-deck/bullet-point text explainer videos.
  - Relying on generic, pre-baked stock audio loops without frame-accurate procedural SFX.
  - Complex 3D photorealistic character modeling that exceeds procedural WebGL/Three.js primitives.

## Alternatives Weighed

1. **Remotion + React Three Fiber (Legacy Approach):**
   * *Rejected:* Produced slow renders, camera-on-card visual artifacts, lack of frame-accurate procedural sound synthesis, and felt like 3D corporate presentations rather than motion graphics.
2. **Pure Video Generative Models (Runway/Sora/Pika):**
   * *Rejected:* Inability to enforce strict vector typography, lack of deterministic frame cues, distorted geometric icons, and zero developer repeatability.
3. **Pure Canvas/SVG + cues.json + mgaudio + Headless Chrome (Selected Standard):**
   * *Accepted:* Fully deterministic, sub-frame motion blur, 48kHz procedurally synthesized stereo audio, rapid local GPU compilation, and award-grade craft benchmarked against Claude Opus 5.5.

## Key Decisions & Staging for Next Steps

1. **Global Plugin Alignment:** Completed. Global agent, auditor, and skill definitions now reflect the new pipeline.
2. **First Production Test:** Produce an original motion graphic introducing the **Motion Graphic AI Agent / Skill itself** using the `01-flat-vector` or `08-morph` engine, enforcing the 1–3 word typographic rule, geometric metaphor, and procedural sound hits.
