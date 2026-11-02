# Visual QC & Contact Sheet Inspection Protocol

To ensure video quality is judged on visual aesthetics and screen-ready beauty (rather than merely passing abstract AST compiler checks), the pipeline employs still-frame contact sheet inspection.

---

## 1. Frame Sampling Strategy
Extract still frames at critical narrative landmarks:
1. **Act Settlement Points:** Frame `actStart + 18` (when hero springs and words settle).
2. **Musical Beat Drops:** Major quarter-note beat frames (`snapToBeat(frame)`).
3. **Transition Co-Presence Apex:** Frame `actEnd` (when both outgoing and incoming scenes are simultaneously visible).
4. ** Climax / High-Energy Moment:** Frame with maximum metric value or vector transformation.

---

## 2. Headless Still-Frame Extraction
Render frames to `.scratch/qc_frames/`:
```bash
npx remotion still src/index.ts <CompositionId> .scratch/qc_frames/frame_act1.png --frame=35
npx remotion still src/index.ts <CompositionId> .scratch/qc_frames/frame_trans1.png --frame=140
```

---

## 3. Visual Review Checklist
The reviewer (or adversarial subagent) evaluates the still frames against these criteria:
- **Legibility Floor:** Are all headlines, labels, and numbers clearly readable at screen distance?
- **Zero Slide Box Check:** Does any large rectangular bordered card enclose the entire act? (If yes $\implies$ REJECT).
- **Zero Corner Clutter Check:** Are there any section labels, telemetry numbers, or watermark text in the corners? (If yes $\implies$ REJECT).
- **Color Saturation:** Are OKLCH gradients vibrant without muddy gray midpoints?
- **Safe Area Verification (9:16):** Are text elements clear of the top 8% and bottom 14% margins?
