# Visual Critique Protocol & 8-Criteria Scorecard

## Overview

The Visual Critique step is decoupled from both the Director and Builder personas.
It evaluates **rendered frames, contact sheets, and motion strips**, strictly judging what is visible and audible on disk—never developer intentions or code comments.

---

## 1. 8-Criteria Scoring Rubric (1–10 Scale)

> **Passing Threshold**: A score of **8** represents publication-grade work suitable for a demanding institutional client.
> **Release Gate**: Verdict is **SHIP** only when **EVERY score $\ge 8$** across at least **3 critique rounds**.

| # | Criterion | 10 Looks Like | Automatic Score Cap |
|---|---|---|---|
| **1** | **Hook (First 2.0s)** | Frame 0 already presents an intentional graphic mark or focal anchor. First core concept reads by 1.5s. Immediate engagement. | Frame 0 is black or empty $\to$ **Max 6** |
| **2** | **Readability at Phone Scale** | All must-read typography is legible at 360px wide (`phone_*.jpg`). Tabular numbers never jitter. Zero clipping in 9:16 safe zones. | CTA or institutional name illegible at 360px $\to$ **Max 6** |
| **3** | **Motion Quality & Physics** | Spring weight and dignified damping. Continuous flow (one thing becomes another). Zero linear pops or unmotivated crossfades. | Fade used as primary enter/exit $\to$ **Max 6**. Visible pop or clamp glitch $\to$ **Max 7** |
| **4** | **Pacing & Event Density** | Something new transforms or arrives every 2–4s (`max_gap_between_visual_events`). Zero static holds $>1.5\text{s}$. Accelerates into conclusion. | Any static dead gap $>4\text{s}$ $\to$ **Max 6** |
| **5** | **Brand & Content Authority** | 100% source-authorized typography, verified medical/scientific claims, exact Persian name orthography, single dominant accent color ramp. | Invented claims or unauthorized English text $\to$ **Max 5** |
| **6** | **Audio & Sync Precision** | Spoken emphasis syllables land with frame-level accuracy ($\pm 1$ frame). Stems mixed to EBU R128 (-14 LUFS, true peak $\le -1\text{dBTP}$). | Sync misalignment $>80\text{ms}$ or loudness $> -12\text{LUFS}$ $\to$ **Max 6** |
| **7** | **Spatial Composition** | Balanced negative space. Clean focal anchor. No card soup. Depth achieved via scale, overlap, and camera perspective rather than fake 3D. | Empty void $>40\%$ of frame for $>2\text{s}$ $\to$ **Max 7** |
| **8** | **Polish & Defect-Free Execution** | Zero clipped glyphs, zero double-exposed swaps, zero lingering carets, zero orphaned lines. Clean head and tail holds. | Double-exposed text collision or clipped descender $\to$ **Max 7** |

---

## 2. 16 Known Failure Modes Checklist

Before issuing a critique score, systematically inspect rendered stills for these fatal traps:

1. [ ] Frame 0 is empty, black, or unfinished.
2. [ ] Audio hit arrives early while the graphic takes 4+ frames to register.
3. [ ] End hold freezes statically for $>1.5\text{s}$ instead of maintaining subtle camera drift.
4. [ ] Headline text wraps into a tall, narrow mobile-column wall instead of filling the landscape canvas.
5. [ ] Incoming scene cuts in before outgoing wipe is fully completed (flicker artifact).
6. [ ] Card soup: every single concept is in a rounded rectangle.
7. [ ] Empty dead zone in 9:16 vertical crop.
8. [ ] Double-exposed text during swaps (outgoing line still visible when incoming lands).
9. [ ] Stray cursor or caret lingering after text entry finishes.
10. [ ] Glyph tops visible through mask boundary on frame 0 of a text reveal.
11. [ ] Orphaned sub-caption remaining on screen after parent header has exited.
12. [ ] Mid-whip blank frame where screen is completely empty during camera transition.
13. [ ] Font fallback occurring (missing Vazirmatn / Dubai font).
14. [ ] Unmotivated camera drift (camera moving without narrative reason).
15. [ ] Subtitle wallpaper (full sentence transcribed instead of 2–3 key words).
16. [ ] Fake premium clutter (unmotivated glow, blurred background orbs, frosted glass on everything).

---

## 3. Critique Round Output Format

Append to `qc/critique_log.md`:

```markdown
## Round N Critique: [Target Version / Shot]

| Criterion | Score (1-10) | Evidence (Timestamps, Frame #, Metric Values) |
|---|---|---|
| Hook (First 2s) | 8 | Frame 0 establishes gold vector anchor; title reads at 0.8s |
| Readability | 9 | Clear at 360px; Vazirmatn rendering crisp; tabular nums active |
| Motion Quality | 8 | TextMaskReveal clean; squash/stretch elastic |
| Pacing | 8 | Event cadence: transitions at 2.4s, 5.1s, 8.2s |
| Content Authority | 10 | 100% matched to approved Persian script |
| Audio Sync | 9 | Hit leads acoustic beat by 2 frames; LUFS = -14.2 |
| Composition | 8 | Single focal anchor, 60% negative space |
| Polish | 8 | Zero clipping, zero double-exposure |

### 3 Worst Problems Identified:
1. ...
2. ...
3. ...

### Concrete Fixes for Round N+1:
1. ...
2. ...
3. ...

**Verdict**: SHIP | ANOTHER ROUND
```
