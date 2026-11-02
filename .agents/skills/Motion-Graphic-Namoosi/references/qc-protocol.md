# TWO-TIER QUALITY CONTROL (QC) PROTOCOL

Adapted from `anything2explainer` and `claude-remotion-skill`.

## 1. Tier 1: Automated Quantitative CV Quality Check
Run the Python test suite against the rendered video and frame stills:
1. `python scripts/selfcheck.py`:
   - Checks code AST against the storyboard.
   - Asserts zero frame gaps between shots.
   - Asserts on-screen text literals are verified in `sources.md`.
2. `python scripts/motion_check.py --frames fin_frames`:
   - Measures frame-to-frame pixel delta in content area.
   - Asserts no static freeze $> 3.0\text{ seconds}$.
   - Asserts post-landing hold $\ge 30\text{ frames}$ ($1.0\text{s}$) before any transition.
3. `python scripts/frame_metrics.py`:
   - Measures hero element bounding box height ($\ge 170\text{px}$).
   - Checks glow area and ensures visual debris count is minimal.

## 2. Tier 2: Agent Visual Inspection
Extract still frames and inspect:
- Contact sheet overview: Read whole video at a glance.
- Contrast and legibility: Is the hero obvious in under 0.5s?
- Typography: Zero text overlaps, clashing colors, or margin clipping.
- Color balance: 60/30/10 rule strictly maintained.
- Audio sync: Do audio hits precede visual hits by 2–3 frames?

## 3. The Fix and Re-render Loop
Never deliver a video with failing QC metrics.
Identify the shot, adjust frame offsets or spring stiffness, re-render, and re-inspect until 100% compliant.
