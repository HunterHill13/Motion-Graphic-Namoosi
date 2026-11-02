import assert from 'node:assert/strict';
import { ImagePlates } from '../lib/image_plates.js';

console.log('--- Testing lib/image_plates.js ---');

// 1. Fallback Monogram Canvas Generator
{
  const fb = ImagePlates.createFallbackPlaceholder('dr_alavi', 256, 256);
  assert.equal(fb.width, 256);
  assert.equal(fb.height, 256);
  console.log('✓ Fallback monogram generator passed');
}

// 2. Preload Handshake with Fallback Safety
{
  // In Node.js, Image is undefined or simulated, should return fallback objects without throwing!
  const manifest = {
    hero: 'assets/non_existent.jpg',
    profile: 'assets/sample.png',
  };
  const loaded = await ImagePlates.preload(manifest);
  assert.ok(loaded.hero, 'hero plate must be populated');
  assert.ok(loaded.profile, 'profile plate must be populated');
  assert.equal(loaded.hero.width, 512);
  console.log('✓ Asynchronous preload with fallback passed');
}

// 3. Aspect Ratio Cover Math & Draw Operations (Mock Context)
{
  const calls = [];
  const mockCtx = {
    save: () => calls.push('save'),
    restore: () => calls.push('restore'),
    translate: (x, y) => calls.push(`translate(${x},${y})`),
    rotate: (r) => calls.push(`rotate(${r})`),
    transform: (a, b, c, d, e, f) => calls.push(`transform(${a},${b},${c},${d},${e},${f})`),
    beginPath: () => calls.push('beginPath'),
    roundRect: (x, y, w, h, r) => calls.push(`roundRect(${x},${y},${w},${h},${r})`),
    rect: (x, y, w, h) => calls.push(`rect(${x},${y},${w},${h})`),
    strokeRect: (x, y, w, h) => calls.push(`strokeRect(${x},${y},${w},${h})`),
    fillRect: (x, y, w, h) => calls.push(`fillRect(${x},${y},${w},${h})`),
    fill: () => calls.push('fill'),
    clip: () => calls.push('clip'),
    drawImage: (img, sx, sy, sw, sh, dx, dy, dw, dh) => {
      calls.push(`drawImage(${dw}x${dh} from ${sw}x${sh})`);
    },
  };

  const mockImg = { width: 1920, height: 1080, naturalWidth: 1920, naturalHeight: 1080 };

  // drawImageCover
  ImagePlates.drawImageCover(mockCtx, mockImg, 0, 0, 400, 400);
  assert.ok(calls.some(c => c.startsWith('drawImage')), 'drawImageCover must call drawImage');
  calls.length = 0;

  // drawSticker
  ImagePlates.drawSticker(mockCtx, mockImg, 100, 100, 300, 300, { strokeWidth: 10, radius: 24 });
  assert.ok(calls.includes('fill'), 'drawSticker must fill white outer shell');
  assert.ok(calls.includes('clip'), 'drawSticker must clip inner image');
  assert.ok(calls.some(c => c.startsWith('drawImage')), 'drawSticker must draw cover image');
  calls.length = 0;

  // drawCollage
  ImagePlates.drawCollage(mockCtx, mockImg, 200, 200, 300, 200, 1.25);
  assert.ok(calls.some(c => c.startsWith('fillRect')), 'drawCollage must draw paper underlay');
  assert.ok(calls.some(c => c.startsWith('strokeRect')), 'drawCollage must draw scissor border');
  assert.ok(calls.some(c => c.startsWith('drawImage')), 'drawCollage must draw image');
  calls.length = 0;

  // drawIsometricPlate
  ImagePlates.drawIsometricPlate(mockCtx, mockImg, 300, 300, 400, 300);
  assert.ok(calls.some(c => c.startsWith('transform')), 'drawIsometricPlate must apply affine matrix');
  assert.ok(calls.some(c => c.startsWith('drawImage')), 'drawIsometricPlate must draw image');
  console.log('✓ Sticker, Collage, and Isometric drawing operations passed');
}

console.log('ALL lib/image_plates.js TESTS PASSED SUCCESSFULLY! 🚀');
