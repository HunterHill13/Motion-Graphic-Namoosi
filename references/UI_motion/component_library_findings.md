# Component Library Integration & Findings (21st.dev / Remocn / RemotionUI)

**Investigation Objective:** Identify reusable, high-end motion primitives and establish normalization rules to prevent design fragmentation.

---

## 1. Findings & Key Differentiation
* **Web Motion (Framer Motion / Tailwind) vs. Video Motion (Remotion):**
  * Many libraries on 21st.dev rely on browser DOM events, continuous requestAnimationFrame loops, or React state hooks that cause non-deterministic skips in video rendering.
  * For programmatic video rendering, motion primitives **must** be deterministic, evaluating strictly from `useCurrentFrame()`, `interpolate()`, and `@remotion/transitions` or custom cubic-bezier math.
* **Remotion-Native Inspirations (Remocn / RemotionUI):**
  * **Architectural Glass Cards:** Clean border glow (`box-shadow: 0 20px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1)`).
  * **Staggered Metric Counters:** Synchronizing mathematical count-up directly to frame numbers without floating-point jitters.
  * **Masked Beam Reveals:** Linear energy tracks with SVG drop-shadow filter glow (`filter: drop-shadow(0 0 12px #38BDF8)`).

---

## 2. Normalization Protocol (Harness Guardrails)
Any component adapted into this studio must strictly obey:
1. **Color Token Enforcement:** Must consume colors exclusively from `DESIGN_SYSTEM.md` (e.g. `#040711`, `#38BDF8`, `#D4AF37`).
2. **Typography Enforcement:** Must use `'YekanBakh'` font family with RTL alignment.
3. **Motion Token Enforcement:** Must use `MOTION_EASINGS.editorial` or `MOTION_EASINGS.snappy` from `src/motion/motionTokens.ts`.
4. **Deterministic Timing:** Zero reliance on uncontrolled `setTimeout` or browser interaction events.
