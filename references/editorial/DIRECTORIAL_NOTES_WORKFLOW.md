# DIRECTORIAL_NOTES_WORKFLOW.md — Director Feedback & Localized Refinement Protocol

**Purpose:** Guide precision refinement without destructive rewrites. When an art director or user provides feedback, the agent interprets notes through local, surgically targeted adjustments.

---

## 1. Directorial Translation Table

| Director Feedback | Meaning & Root Cause | Exact Surgical Adjustment |
|---|---|---|
| *"Slow this zoom by 30%"* | Camera motion feels hurried | Increase interpolation duration by $1.3\times$ or adjust end zoom from $1.03 \to 1.02$. |
| *"Hold this frame 12 frames longer"* | Information leaves screen before comprehension | Shift exit interpolation start: e.g. `[810, 860] -> [822, 872]`. |
| *"Remove camera movement from this scene"* | Parallax or zoom distracts from text | Set camera keyframe values to static identity (`cx: 960, cy: 540, zoom: 1.0, rotX: 0, rotY: 0`). |
| *"Move focal object 80px left"* | Asymmetric balance or margin clearance | Update container `left` or `transform: translateX(-80px)`. |
| *"Delay secondary label by 8 frames"* | All text elements appear simultaneously | Add $+8$ offset to secondary label's `frame` interpolation range. |
| *"Make this transition 10 frames longer"* | Scene handoff feels clipped | Extend transition overlap window from 30f to 40f in `Sequence` duration and exit interpolation. |
| *"Make the handoff more obvious"* | Morph continuity bridge is too faint | Increase peak bridge opacity or broaden morph width curve in `transitions.tsx`. |
| *"Reduce background motion by 50%"* | Background grid or radial glow competes with text | Halve opacity of background elements (`rgba(..., 0.08) -> rgba(..., 0.04)`). |
| *"Increase contrast of primary number"* | Score number does not pop immediately | Bump font weight to 900, set font size to 64px, and apply subtle glow filter. |

---

## 2. Invariant Guardrails During Refinements
1. **Never change the Canonical Script:** 0 text rewrites or summarizations.
2. **Never break working Stems:** Maintain single continuous voice narration and ducked score.
3. **Local Scope Only:** Modifying Scene 3 must never alter code in Scene 1 or Scene 5.
