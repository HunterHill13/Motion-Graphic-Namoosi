# PRE-DELIVERY QUALITY CONTROL (QC) CHECKLIST

Before presenting any render (pilot or final) to the client or user, the agent must systematically verify every item below.

---

## 1. Quantitative Automation Gate (Run via Python)
- [ ] `python scripts/selfcheck.py` executed:
  - 0 timeline gaps between shots
  - 0 glitch whitelist violations
  - 100% on-screen strings verified against `sources.md`
- [ ] `python scripts/motion_check.py` executed:
  - Longest static freeze across all shots $\le 3.0\text{ seconds}$
  - Post-landing stable hold $\ge 30\text{ frames}$ ($1.0\text{s}$)
- [ ] `python scripts/frame_metrics.py` executed:
  - Hero bounding height $\ge 170\text{px}$
  - Zero background visual debris / uncontained noise

---

## 2. Cinematography & Motion Review
- [ ] Zero linear interpolation (`interpolate` calls clamped with smooth bezier or spring).
- [ ] Entrances combine 2–3 properties (opacity + translate + scale).
- [ ] Staggered timing: Child elements offset by 3–6 frames; nothing enters simultaneously.
- [ ] Exits animated cleanly, faster than entrances ($10-14\text{f}$).
- [ ] Active Camera: Every shot has an active `CameraRig` executing subtle continuous push/pull ($1.00 \to 1.05$).
- [ ] Motion Continuity: No naked hard cuts; sequence boundaries utilize designed transitions.
- [ ] Hand-off State Machine: Preceding hero elements yield visual focus via `Live demoteAt`.

---

## 3. Typography & Hierarchy
- [ ] Strict 3-tier visual hierarchy maintained: Hero $\to$ Secondary $\to$ Environment.
- [ ] 60/30/10 color rule respected; $\le 1$ hero-colored or glowing element per frame.
- [ ] Hero text uses display/hero typeface with font weight $\ge 600$.
- [ ] Critical text remains strictly within the 12% vertical and 8% horizontal safe margins.
- [ ] Zero text clipping, overflowing boxes, or uncontained line wraps.

---

## 4. Audio & Sound Design
- [ ] Voiceover is clear, unclipped, and ducked at appropriate levels.
- [ ] Sound effect hits land 2–3 frames early relative to visual impact for biological perception sync.
- [ ] Background music bed volume kept at $0.20-0.28$, ducked under dialogue.

---

## 5. Technical Integrity
- [ ] Rendered at exact target resolution ($1920\times 1080$ or $1080\times 1920$) and frame rate ($30\text{ fps}$).
- [ ] Zero dropped frames, zero flickering artifacts.
- [ ] H.264 video encoded at `--crf 16` with high-quality pixel format `yuv420p`.
