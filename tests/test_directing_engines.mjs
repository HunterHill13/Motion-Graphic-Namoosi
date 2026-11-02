/**
 * tests/test_directing_engines.mjs
 * Comprehensive automated verification suite for Flat Vector & Shape Morph directing engines.
 */

import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Morph, resamplePoly, orient, area, centroid, bestShift, alignTo, lerpP, circ, capsule, oklab, fromOklab, mixC } from '../lib/morph.js';
import { MotionCraft, pop, spring } from '../lib/motion.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

console.log('--- RUNNING DIRECTING ENGINES VERIFICATION SUITE ---');

// ---------------------------------------------------------------- Test 1: resamplePoly Equidistant Arc-Length
{
  console.log('Test 1: resamplePoly produces exactly 240 equidistant points on unit square...');
  const square = [
    [0, 0],
    [100, 0],
    [100, 100],
    [0, 100],
  ];
  const res = resamplePoly(square, 240);
  assert.equal(res.length, 240, 'Vertex count must be exactly 240');

  const expectedStep = 400 / 240; // Perimeter = 400
  for (let i = 0; i < res.length; i++) {
    const p1 = res[i];
    const p2 = res[(i + 1) % res.length];
    const dist = Math.hypot(p2[0] - p1[0], p2[1] - p1[1]);
    assert(
      Math.abs(dist - expectedStep) < 0.001,
      `Step distance at index ${i} (${dist.toFixed(5)}) diverged from expected (${expectedStep.toFixed(5)}) by > 1e-3`
    );
  }
  console.log('  ✓ resamplePoly passed.');
}

// ---------------------------------------------------------------- Test 2: bestShift & orient
{
  console.log('Test 2: bestShift and orient maintain correct phase alignment and winding order...');
  const circleA = circ(0, 0, 100, 240);
  assert.equal(circleA.length, 240);

  // Circularly shifted by 60 positions
  const circleB = circleA.map((_, i) => circleA[(i + 60) % 240]);
  const shift = bestShift(circleA, circleB);
  assert.equal(shift, 180, `Shift of circleB relative to circleA must be 180, got ${shift}`);

  const aligned = alignTo(circleA, circleB);
  assert.deepEqual(aligned[0], circleA[0], 'Aligned index 0 must match circleA[0]');

  // Reverse winding test
  const circleRev = circleA.slice().reverse();
  assert(area(circleRev) < 0, 'Reversed circle must have negative signed area');
  const oriented = orient(circleRev);
  assert(area(oriented) > 0, 'orient() must restore positive (clockwise/standard) signed area');
  console.log('  ✓ bestShift and orient passed.');
}

// ---------------------------------------------------------------- Test 3: mixC Oklab Chroma Midpoint
{
  console.log('Test 3: mixC in Oklab space prevents desaturation midpoint dips between complementary colors...');
  const red = '#FF0000';
  const cyan = '#00FFFF';
  const mid = mixC(red, cyan, 0.5);
  const [L, a, b] = oklab(mid);
  const chroma = Math.hypot(a, b);

  // In sRGB, midpoint of #FF0000 and #00FFFF is gray #808080 (chroma = 0.0).
  // In Oklab, chroma must remain elevated (> 0.04).
  assert(
    chroma > 0.04,
    `Midpoint chroma in Oklab (${chroma.toFixed(4)}) dipped below minimum threshold 0.04`
  );
  console.log(`  ✓ mixC Oklab chroma: ${chroma.toFixed(4)} > 0.04.`);
}

// ---------------------------------------------------------------- Test 4: capsule Geometry & Centroid
{
  console.log('Test 4: capsule parametric rounded pill geometry...');
  const cap = capsule(0, 0, 200, 100, 50, 240);
  assert.equal(cap.length, 240, 'Capsule vertex count must be exactly 240');

  const xs = cap.map((p) => p[0]);
  const ys = cap.map((p) => p[1]);
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys), maxY = Math.max(...ys);

  assert(Math.abs(maxX - minX - 200) < 0.05, `Bounding width must be 200, got ${maxX - minX}`);
  assert(Math.abs(maxY - minY - 100) < 0.05, `Bounding height must be 100, got ${maxY - minY}`);

  const [cx, cy] = centroid(cap);
  assert(Math.abs(cx) < 0.001 && Math.abs(cy) < 0.001, `Centroid must be (0, 0), got (${cx}, ${cy})`);
  console.log('  ✓ capsule geometry passed.');
}

// ---------------------------------------------------------------- Test 5: lib/motion.js pop() Pinning
{
  console.log('Test 5: lib/motion.js pop() settles strictly to [1.0, 0.0] beyond pin threshold...');
  const [scale, squash] = pop(1.0, 0.0, 2.4, 0.42, 0.12, 0.9);
  assert.equal(scale, 1, `Scale must be pinned to exactly 1.0, got ${scale}`);
  assert.equal(squash, 0, `Squash must be pinned to exactly 0.0, got ${squash}`);
  console.log('  ✓ pop() pinning passed.');
}

// ---------------------------------------------------------------- Test 6: Stills Manifest & File Validation
{
  console.log('Test 6: Validating harness --stills output and manifest.json for benchmarks...');
  const demos = ['01-flat-vector', '08-morph'];

  for (const demo of demos) {
    const manifestPath = path.join(rootDir, 'demos', demo, 'out', 'stills', 'manifest.json');
    assert(fs.existsSync(manifestPath), `Manifest must exist at ${manifestPath}`);

    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    assert(manifest.stills && manifest.stills.length >= 5, `Demo ${demo} must have >= 5 stills, got ${manifest.stills.length}`);

    for (const item of manifest.stills) {
      assert(item.isNonBlank === true, `Still ${item.filename} in ${demo} failed non-blank check`);
      const imgPath = path.join(rootDir, 'demos', demo, 'out', 'stills', item.filename);
      assert(fs.existsSync(imgPath), `Still image ${imgPath} must exist on disk`);
      const stat = fs.statSync(imgPath);
      assert(stat.size > 1024, `Still image ${imgPath} size (${stat.size}B) must be > 1KB`);
    }
    console.log(`  ✓ Demo ${demo} stills manifest verified (${manifest.stills.length} non-blank stills).`);
  }
}

console.log('\n--- ALL DIRECTING ENGINES VERIFICATION TESTS PASSED (6/6) ---');
