# Supercharging the Cinematic Motion Graphics Director Engine

* **Author:** Senior Motion Director AI Agent
* **Status:** Approved & Implemented
* **Date:** 2026-11-01
* **Context Ingested:** `concepts_brief.md`
* **Dedicated Agent Repository:** [`HunterHill13/Motion-Graphic-Agent`](https://github.com/HunterHill13/Motion-Graphic-Agent.git)
* **Skill & Remotion Engine Repository:** [`HunterHill13/Motion-Graphic-Namoosi`](https://github.com/HunterHill13/Motion-Graphic-Namoosi.git)

--------------------------------------------------------------------------------

## Overview

This technical design document specifies the architectural overhaul of the `cinematic-motion-director` skill system. By assimilating proven visual mechanics from six industry-leading open-source motion graphics repositories (`iart-ai/motion-skills`, `what-if-animation`, `tool-reel-system`, `anthropics/skills`, `awesome-cursorrules`, and `awesome-mcp-servers`), this upgrade establishes an uncompromising broadcast-quality standard for programmatic video generation in Remotion.

The upgraded engine consolidates all visual motion recipes, motivated lighting paradigms, polymorphic cut-pacing models, and a mandatory pre-flight visual contact sheet verification loop directly into the unified `cinematic-motion-director` skill.

--------------------------------------------------------------------------------

## The Problem

Our Remotion pipeline (`cinematic-motion-director`) achieved strong structural rigor in spring physics and typography, but suffered from four broadcast-quality bottlenecks:

1. **Blind Video Rendering (Absence of Visual Contact Sheets):** Full 30-second MP4 videos were rendered without intermediate visual sanity checks. Rendering defects (font blowups, clipping, unmotivated layouts) wasted compute and latency before any human or AI agent spotted them.
2. **Pacing Rigidity & Lack of Sub-Word Cut Cues:** Cuts were timed mechanically to music beats without adapting to viral short-form pacing laws (20–27 cuts/min, alternating shot sizes, zero static holds >3s) or academic documentary pacing (8–15 cuts/min). Cuts did not land on word-anchored cues.
3. **Limited Kinetic Repertoire:** Visual elements entered through standard spring transitions rather than broadcast-grade kinetic recipes (masked wipes, scale-settle, split-flap counters, and chapter ordinal reset cards).
4. **Flat Backdrops vs. Motivated Practical Light Pools:** Scenes lacked identifiable practical light sources (pendant lamps, windows, terminal beams) with volumetric dust motes, directional rim highlights, and depth-of-field separation.

--------------------------------------------------------------------------------

## Goals

* **Goal 1: Mandatory Pre-Flight Visual Verification.** Enforce automated rendering and inspection of a multi-panel captioned storyboard sheet (`out/storyboard.jpg`) and a frame burst flipbook grid (`out/motiongrid.png`) via Remotion stills before any full MP4 render is initiated.
* **Goal 2: Monolithic Ingestion of Motion Recipes.** Integrate four core visual components into `src/motion/recipes/` and `src/motion/actors/`: `OrdinalChapterCard.tsx`, `MotivatedLightPool.tsx`, `TriFontKineticBlock.tsx`, and `ProceduralDataChart.tsx`.
* **Goal 3: Polymorphic Adaptive Cut Pacing.** Implement an engine capable of auto-selecting between Fast-Paced Viral (20–27 cuts/min, max 2.5s per shot, zero static holds over 3s) and Long-Form Documentary (8–15 cuts/min, continuous camera travel, deep diagrams) based on the creative brief.
* **Goal 4: Complete Reference & Standard Hardening.** Ingest four authoritative reference manuals into `.agents/skills/cinematic-motion-director/references/` covering camera grammar, kinetic reveals, viral teardowns, and anti-cliche principles, while updating `SKILL.md` and `resources/rubrics/motion-director-rubric.md`.
* **Goal 5: Dedicated Agent Repository Separation.** Keep all agent personas, memory, rubrics, and orchestration in `Motion-Graphic-Agent.git`, strictly separating agent governance from skill rendering assets.

--------------------------------------------------------------------------------

## Non-Goals

* **Non-Goal 1: Multi-Skill Package Fragmentation.** We do not create separate standalone micro-skills. All recipes and grammar guides live monolithically within `cinematic-motion-director`.
* **Non-Goal 2: Audio Loudness Verification Scripts.** We do not implement external LUFS audio measurement or mix-check scripts (`mixcheck.py`), as our existing audio engine is established and verified.
* **Non-Goal 3: External MCP Server Dependencies.** We do not delegate image processing or video editing to external MCP servers; all operations execute deterministically via local Node.js, Remotion, and FFmpeg.

--------------------------------------------------------------------------------

## Critical User Journeys (CUJs)

### CUJ 1: High-Retention Viral Reel Production

* **Given:** A short-form technical or educational script cued to a fast audio track.
* **When:** The user runs `cinematic-motion-director` with the brief.
* **Then:**
  1. The engine selects the Fast Viral pacing profile (20–27 cuts/min, alternating framing: Wide $\rightarrow$ Macro $\rightarrow$ Medium $\rightarrow$ Close-up).
  2. The engine generates `out/storyboard.jpg` and `out/motiongrid.png`.
  3. The auditor validates light sources, rim lighting, ordinal scale-settle cards, and zero static holds over 3s.
  4. Only upon 100% pass, the master MP4 is rendered.

### CUJ 2: In-Depth Documentary / Academic Motion Picture

* **Given:** A medical or scientific research script with complex clinical data.
* **When:** The user runs `cinematic-motion-director` with the brief.
* **Then:**
  1. The engine selects the Documentary pacing profile (8–15 cuts/min, continuous slow dolly, deep diagrams).
  2. Living procedural data charts and axonometric isometric plates animate smoothly on an open canvas.
  3. Pre-flight storyboard stills verify zero data rounding and exact statistical representation before final MP4 rendering.

--------------------------------------------------------------------------------

## Implemented Architecture

1. **Remotion Visual Components:**
   - [`OrdinalChapterCard.tsx`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/src/motion/recipes/OrdinalChapterCard.tsx)
   - [`MotivatedLightPool.tsx`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/src/motion/actors/MotivatedLightPool.tsx)
   - [`TriFontKineticBlock.tsx`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/src/motion/typography/TriFontKineticBlock.tsx)
   - [`ProceduralDataChart.tsx`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/src/motion/recipes/ProceduralDataChart.tsx)
2. **Editorial Pacing Engine:**
   - [`PacingEngine.ts`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/src/motion/editorial/PacingEngine.ts)
3. **Pre-Flight Visual Verification Scripts:**
   - [`render_storyboard_sheet.ts`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/scripts/render_storyboard_sheet.ts)
   - [`render_motiongrid_flipbook.ts`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/scripts/render_motiongrid_flipbook.ts)
4. **Reference Manuals:**
   - [`look_and_pacing_grammar.md`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/.agents/skills/cinematic-motion-director/references/look_and_pacing_grammar.md)
   - [`reveal_recipes_catalog.md`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/.agents/skills/cinematic-motion-director/references/reveal_recipes_catalog.md)
   - [`viral_reel_edit_teardown.md`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/.agents/skills/cinematic-motion-director/references/viral_reel_edit_teardown.md)
   - [`anti_cliche_design_principles.md`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/.agents/skills/cinematic-motion-director/references/anti_cliche_design_principles.md)
5. **Skill Specification:**
   - [`cinematic-motion-director/SKILL.md`](file:///g:/دانشگاه/کمیته%20تحقیقاتی/فیلم%20ها%20هفتگی/اسکیل%20موشن%20گرافیک/.agents/skills/cinematic-motion-director/SKILL.md)
