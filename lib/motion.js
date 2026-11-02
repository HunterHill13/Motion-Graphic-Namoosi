/**
 * lib/motion.js - Canonical Motion Craft Kinematics Engine
 * Calibrated against Claude Opus 5.5 / Buck / Ordinary Folk / Apple Keynote
 * Zero external dependencies. Browser & Node.js compatible.
 */

// Math helpers
const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
const lerp = (a, b, u) => a + (b - a) * u;
const inv = (a, b, x) => clamp((x - a) / (b - a));

/**
 * Cubic Bezier curve evaluator with Newton-Raphson numerical inversion.
 * Exact mathematical formulation used in CSS transition-timing-function.
 */
export function bezier(x1, y1, x2, y2) {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const sx = (t) => ((ax * t + bx) * t + cx) * t;
  const sy = (t) => ((ay * t + by) * t + cy) * t;
  const dx = (t) => (3 * ax * t + 2 * bx) * t + cx;

  return (u) => {
    if (u <= 0) return 0;
    if (u >= 1) return 1;
    let t = u;
    for (let i = 0; i < 10; i++) {
      const d = dx(t);
      if (Math.abs(d) < 1e-6) break;
      t = clamp(t - (sx(t) - u) / d);
    }
    return sy(t);
  };
}

/**
 * Canonical motion design overshoot curve: cubic-bezier(0.34, 1.56, 0.64, 1).
 * Smooth zero initial velocity with elastic overshoot up to ~1.08 before settling.
 */
export const overshootEase = bezier(0.34, 1.56, 0.64, 1);

/**
 * Closed-form damped harmonic oscillator position (0 -> 1).
 * Continuous position and continuous velocity starting at 0 when t = 0.
 * @param {number} t - Elapsed seconds since trigger
 * @param {number} f - Frequency in Hz (cycles/sec, default 2.0)
 * @param {number} z - Damping ratio zeta (default 0.4, under-damped bounce)
 */
export function spring(t, f = 2.0, z = 0.4) {
  if (t <= 0) return 0;
  const w = 2 * Math.PI * f;
  const a = z * w;
  const b = w * Math.sqrt(Math.max(0.0001, 1 - z * z));
  return 1 - Math.exp(-a * t) * (Math.cos(b * t) + (a / b) * Math.sin(b * t));
}

/**
 * Closed-form damped harmonic oscillator velocity (derivative of spring).
 */
export function springV(t, f = 2.0, z = 0.4) {
  if (t <= 0) return 0;
  const w = 2 * Math.PI * f;
  const a = z * w;
  const b = w * Math.sqrt(Math.max(0.0001, 1 - z * z));
  return Math.exp(-a * t) * ((w * w) / b) * Math.sin(b * t);
}

/**
 * Damped impulse kick (single shock oscillation).
 */
export function kick(t, t0, f = 3.0, z = 0.35) {
  if (t <= t0) return 0;
  const w = 2 * Math.PI * f;
  const tt = t - t0;
  return Math.exp(-z * w * tt) * Math.sin(w * Math.sqrt(Math.max(0.0001, 1 - z * z)) * tt);
}

/**
 * Spring pop with velocity-driven squash & stretch.
 * Returns [scale, k_squash], pinned to exactly 1.0 and 0.0 after `pin` seconds
 * to prevent sub-pixel shimmering during end holds.
 */
export function pop(t, t0, f = 2.4, z = 0.42, amt = 0.12, pin = 0.9) {
  const tt = t - t0;
  if (tt <= 0) return [0, 0];
  let s = spring(tt, f, z);
  let k = clamp((springV(tt, f, z) / (2 * Math.PI * f)) * amt * 2, -0.3, 0.3);
  if (tt >= pin) {
    s = 1;
    k = 0;
  } else if (tt > pin * 0.7) {
    const w = (tt - pin * 0.7) / (pin * 0.3);
    s = lerp(s, 1, w);
    k = lerp(k, 0, w);
  }
  return [s, k];
}

/**
 * Anticipation: Pulls back in reverse direction before explosive launch.
 * Guaranteed zero at t <= t0 and t >= t0 + dur.
 * @param {number} t - Current time
 * @param {number} t0 - Anticipation start time
 * @param {number} dur - Anticipation duration (seconds)
 * @param {number} amount - Peak pullback magnitude (0.04 - 0.10)
 */
export function anticipation(t, t0, dur = 0.2, amount = 0.08) {
  if (dur <= 0 || t < t0 || t > t0 + dur) return 0;
  const progress = (t - t0) / dur;
  return -amount * Math.sin(progress * Math.PI);
}

/**
 * Stagger helper: Calculates delayed arrival timestamp for indexed list elements.
 */
export function stagger(index, baseTime = 0.5, delayFrames = 3, fps = 30) {
  return baseTime + (index * delayFrames) / fps;
}

/**
 * Executes a draw callback with dynamic squash & stretch aligned to the motion vector (vx, vy).
 * Scales parallel axis by (1 + speed * k) and perpendicular axis by 1 / sqrt(stretch)
 * to maintain constant visual area (incompressible physical deformation).
 */
export function applySquashStretch(ctx, x, y, vx, vy, k = 0.0015, drawFn) {
  const speed = Math.hypot(vx, vy);
  const stretch = Math.max(0.2, 1 + speed * k);
  const squash = 1 / Math.sqrt(stretch);
  const angle = Math.atan2(vy, vx);

  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle);
  ctx.scale(stretch, squash);
  ctx.rotate(-angle);
  ctx.translate(-x, -y);
  drawFn();
  ctx.restore();
}

/**
 * Element-driven circular shape wipe mask.
 * Clips the canvas to an expanding/contracting circle centered at (cx, cy).
 */
export function clipShapeWipe(ctx, cx, cy, radius, renderFn) {
  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy, Math.max(0, radius), 0, Math.PI * 2);
  ctx.clip();
  renderFn();
  ctx.restore();
}

export const MotionCraft = {
  bezier,
  overshootEase,
  spring,
  springV,
  kick,
  pop,
  anticipation,
  stagger,
  applySquashStretch,
  clipShapeWipe,
};

// Universal export pattern for browser window and Node.js
if (typeof window !== 'undefined') window.MotionCraft = MotionCraft;
if (typeof module !== 'undefined' && module.exports) module.exports = { MotionCraft };
