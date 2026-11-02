import assert from 'node:assert/strict';
import {
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
  MotionCraft,
} from '../lib/motion.js';

console.log('--- Testing lib/motion.js ---');

// 1. Bezier & Overshoot Ease
{
  assert.equal(overshootEase(0), 0, 'overshootEase(0) must be 0');
  assert.equal(overshootEase(1), 1, 'overshootEase(1) must be 1');
  const mid = overshootEase(0.6);
  assert.ok(mid > 1.0, `overshootEase(0.6) must bounce above 1.0 (got ${mid})`);
  assert.ok(mid < 1.25, `overshootEase(0.6) must not explode beyond 1.25 (got ${mid})`);
  console.log('✓ Bezier & Overshoot Ease passed');
}

// 2. Spring Physics
{
  assert.equal(spring(0), 0, 'spring(0) must be 0');
  const sAfter1s = spring(1.0);
  assert.ok(Math.abs(sAfter1s - 1.0) < 0.05, `spring(1.0) must settle close to 1.0 (got ${sAfter1s})`);

  const v0 = springV(0);
  assert.equal(v0, 0, 'springV(0) initial velocity must be 0');
  const vPeak = springV(0.1);
  assert.ok(vPeak > 0, `springV(0.1) should show positive initial velocity (got ${vPeak})`);
  console.log('✓ Spring & Spring Velocity passed');
}

// 3. Kick impulse
{
  assert.equal(kick(0, 1.0), 0, 'kick before trigger must be 0');
  assert.equal(kick(1.0, 1.0), 0, 'kick at trigger must be 0');
  assert.ok(Math.abs(kick(1.1, 1.0)) > 0, 'kick after trigger must oscillate');
  console.log('✓ Kick impulse passed');
}

// 4. Pop (Displacement + Squash/Stretch)
{
  const [s0, k0] = pop(0, 0.5);
  assert.equal(s0, 0);
  assert.equal(k0, 0);

  const [sPin, kPin] = pop(2.0, 0.5, 2.4, 0.42, 0.12, 0.9);
  assert.equal(sPin, 1.0, 'pop must be pinned to 1.0 after pin time');
  assert.equal(kPin, 0.0, 'pop squash must be pinned to 0.0 after pin time');
  console.log('✓ Pop displacement & squash pinning passed');
}

// 5. Anticipation
{
  assert.equal(anticipation(0, 0.2, 0.2, 0.08), 0, 'anticipation before t0 must be 0');
  assert.equal(anticipation(0.5, 0.2, 0.2, 0.08), 0, 'anticipation after t0+dur must be 0');
  assert.equal(anticipation(0.2, 0.2, 0.0, 0.08), 0, 'anticipation with dur <= 0 must be 0');
  const midPull = anticipation(0.3, 0.2, 0.2, 0.08);
  assert.ok(midPull < 0, `anticipation midpoint must be negative pullback (got ${midPull})`);
  assert.ok(Math.abs(midPull - -0.08) < 1e-4, `anticipation midpoint must reach -amount (got ${midPull})`);
  console.log('✓ Anticipation pullback passed');
}

// 6. Stagger
{
  assert.equal(stagger(0, 0.5, 3, 30), 0.5);
  assert.equal(stagger(1, 0.5, 3, 30), 0.6);
  assert.equal(stagger(2, 0.5, 3, 30), 0.7);
  console.log('✓ Stagger timestamps passed');
}

// 7. applySquashStretch & clipShapeWipe (Mock Context)
{
  const calls = [];
  const mockCtx = {
    save: () => calls.push('save'),
    restore: () => calls.push('restore'),
    translate: (x, y) => calls.push(`translate(${x},${y})`),
    rotate: (rad) => calls.push(`rotate(${rad.toFixed(2)})`),
    scale: (sx, sy) => calls.push(`scale(${sx.toFixed(2)},${sy.toFixed(2)})`),
    beginPath: () => calls.push('beginPath'),
    arc: (cx, cy, r, s, e) => calls.push(`arc(${cx},${cy},${r})`),
    clip: () => calls.push('clip'),
  };

  let drawn = false;
  applySquashStretch(mockCtx, 100, 200, 50, 0, 0.01, () => {
    drawn = true;
  });
  assert.ok(drawn, 'applySquashStretch must invoke draw callback');
  assert.ok(calls.includes('save') && calls.includes('restore'));
  assert.ok(calls.some(c => c.startsWith('scale')), 'must execute scale transformation');

  calls.length = 0;
  let wiped = false;
  clipShapeWipe(mockCtx, 960, 540, 250, () => {
    wiped = true;
  });
  assert.ok(wiped, 'clipShapeWipe must invoke render callback');
  assert.ok(calls.includes('clip'), 'clipShapeWipe must call ctx.clip');
  console.log('✓ applySquashStretch and clipShapeWipe passed');
}

console.log('ALL lib/motion.js TESTS PASSED SUCCESSFULLY! 🚀');
