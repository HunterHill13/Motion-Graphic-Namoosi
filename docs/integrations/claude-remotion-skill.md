# External Integration Audit: Claude Remotion Skill (`haidrrrry/claude-remotion-skill`)

**Repository:** `https://github.com/haidrrrry/claude-remotion-skill`  
**License:** MIT / Permissive Open Source  
**Audit Date:** 2026-10-04  
**Audit Purpose:** Extract motion design foundations, spring choreography rules, and iterative QC loop patterns for Antigravity + Gemini.

---

## 1. Useful Concepts Extracted

1. **Spring Choreography over Linear Interpolation:**
   - Strict ban on static linear transitions (`t => a + t*(b-a)`).
   - Use Remotion `spring()` with explicit `{ damping, mass, stiffness }` parameters to reflect physical material properties (heavy organelles vs. light particles).
2. **Staggered Orchestration:**
   - Multi-element reveals must always use calculated delays (e.g., 3–5 frame cascades) to establish visual reading hierarchy.
3. **Continuous Film Metaphor:**
   - Handheld micro-camera drift (`LivingCameraRig`) operating across all frames to prevent frozen-screen artifacts.
4. **Mandatory Render $\to$ Inspect $\to$ Fix Loop:**
   - Code compilation (`tsc` or `npm run build`) is merely a syntax check, not a verification of visual motion quality. Automated frame extraction and visual review are strictly required.

---

## 2. Reusable Code & Patterns
- Remotion `interpolate()` clamped configurations.
- Multi-layer spatial compositing (depth planes with differential blur).
- Frame-rate independent timing calculations (`frame / fps`).

---

## 3. Incompatible Concepts & Project Adaptations
- **Incompatible:** Claude Remotion Skill defaults to 16:9 landscape web explainers with English-first font rendering.
- **Project Adaptation:**
  - Full dual-aspect authority (`AspectRatioDirector` supporting 9:16 Shorts/TikTok and 1:1).
  - Persian typography integration with Dubai font and RTL bidi rendering.
  - Scientific biomolecular vector mode rather than standard SaaS/web UI elements.
