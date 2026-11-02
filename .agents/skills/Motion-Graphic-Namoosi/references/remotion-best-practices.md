# REMOTION BEST PRACTICES & LIFECYCLE RULES

Adapted from official Remotion skills (`remotion-dev/skills`).

## 1. Frame-Deterministic React Code
- Always use `useCurrentFrame()` and `useVideoConfig()`.
- Remotion renders non-linearly (frames can be requested in arbitrary order or in parallel across CPU threads).
- Never use `Math.random()`, `Date.now()`, or mutable external state without deterministic seeding.
- Never use CSS transitions or CSS `@keyframes` that rely on wall-clock time. Every animation state must be a pure function of `frame`.

## 2. Seek-Safety & Clamp Rules
- Always clamp interpolation boundaries:
  ```tsx
  interpolate(frame, [0, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  ```
- Use `spring()` with `fps` passed explicitly:
  ```tsx
  spring({ frame, fps, config: { damping: 18, stiffness: 90 } });
  ```

## 3. High-Quality Rendering Flags
- Target: `--codec h264 --crf 16 --pixel-format yuv420p`
- Concurrency: Set based on host CPU cores (default 4–6).
- Image format: JPEG 90 for fast render; PNG for heavy transparency.
