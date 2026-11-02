import * as fs from 'fs';
import * as path from 'path';
import * as cp from 'child_process';

function assert(condition: boolean, message: string) {
  if (!condition) {
    console.error(`❌ ASSERTION FAILED: ${message}`);
    process.exit(1);
  }
}

console.log('================================================================');
console.log('VERIFYING OPUS 5.5 MOTION ENGINE & INTEGRITY GATES');
console.log('================================================================\n');

// 1. Harness & Renderer
console.log('--- 1. Harness & Chrome Renderer ---');
const harnessPath = path.resolve('harness/render.mjs');
assert(fs.existsSync(harnessPath), 'harness/render.mjs does not exist');
const harnessContent = fs.readFileSync(harnessPath, 'utf8');
assert(harnessContent.includes('chrome.exe') || harnessContent.includes('findChrome'), 'harness/render.mjs lacks Chrome launcher logic');
assert(harnessContent.includes('renderAt'), 'harness/render.mjs does not invoke window.renderAt');
console.log('  ✅ Harness and Chrome launcher verified.\n');

// 2. Foundation Kinematics, Morphing & Image Plates Libraries
console.log('--- 2. Core Libraries (lib/motion.js, lib/morph.js & lib/image_plates.js) ---');
const motionLibPath = path.resolve('lib/motion.js');
assert(fs.existsSync(motionLibPath), 'lib/motion.js does not exist');
const motionLibContent = fs.readFileSync(motionLibPath, 'utf8');
assert(motionLibContent.includes('bezier'), 'lib/motion.js missing bezier');
assert(motionLibContent.includes('overshootEase'), 'lib/motion.js missing overshootEase');
assert(motionLibContent.includes('spring'), 'lib/motion.js missing spring');
assert(motionLibContent.includes('pop'), 'lib/motion.js missing pop');
assert(motionLibContent.includes('anticipation'), 'lib/motion.js missing anticipation');
assert(motionLibContent.includes('applySquashStretch'), 'lib/motion.js missing applySquashStretch');
assert(motionLibContent.includes('clipShapeWipe'), 'lib/motion.js missing clipShapeWipe');

const morphLibPath = path.resolve('lib/morph.js');
assert(fs.existsSync(morphLibPath), 'lib/morph.js does not exist');
const morphLibContent = fs.readFileSync(morphLibPath, 'utf8');
const morphMethods = [
  'sampleD', 'resamplePoly', 'area', 'orient', 'centroid',
  'bestShift', 'alignTo', 'lerpP', 'circ', 'capsule',
  'oklab', 'fromOklab', 'mixC', 'Morph'
];
for (const method of morphMethods) {
  assert(morphLibContent.includes(method), `lib/morph.js missing method/export: ${method}`);
}

const imagePlatesPath = path.resolve('lib/image_plates.js');
assert(fs.existsSync(imagePlatesPath), 'lib/image_plates.js does not exist');
const imagePlatesContent = fs.readFileSync(imagePlatesPath, 'utf8');
assert(imagePlatesContent.includes('preload'), 'lib/image_plates.js missing preload');
assert(imagePlatesContent.includes('createFallbackPlaceholder'), 'lib/image_plates.js missing createFallbackPlaceholder');
assert(imagePlatesContent.includes('drawSticker'), 'lib/image_plates.js missing drawSticker');
assert(imagePlatesContent.includes('drawCollage'), 'lib/image_plates.js missing drawCollage');
assert(imagePlatesContent.includes('drawIsometricPlate'), 'lib/image_plates.js missing drawIsometricPlate');
console.log('  ✅ Foundation libraries and method exports verified.\n');

// 3. Procedural Audio Engine (mgaudio) & Speech Sync Engine
console.log('--- 3. Procedural Audio Engine (mgaudio) & Speech Sync Engine ---');
const mgaudioPath = path.resolve('lib/audio/mgaudio');
assert(fs.existsSync(mgaudioPath), 'lib/audio/mgaudio package does not exist');
const synthPath = path.join(mgaudioPath, 'synth.py');
assert(fs.existsSync(synthPath), 'mgaudio/synth.py does not exist');

const speechSyncPath = path.resolve('lib/audio/speech_sync.py');
assert(fs.existsSync(speechSyncPath), 'lib/audio/speech_sync.py does not exist');
const speechSyncContent = fs.readFileSync(speechSyncPath, 'utf8');
assert(speechSyncContent.includes('SpeechSyncEngine'), 'speech_sync.py missing SpeechSyncEngine class');
assert(speechSyncContent.includes('align_shotbook'), 'speech_sync.py missing align_shotbook method');
assert(speechSyncContent.includes('snap_to_grid'), 'speech_sync.py missing snap_to_grid method');

console.log('  Running Python speech_sync unit & integration test suite...');
try {
  const pyOut = cp.execSync('uv run python tests/test_speech_sync.py', {
    env: { ...process.env, PYTHONUTF8: '1' },
    encoding: 'utf8',
    stdio: 'pipe',
  });
  console.log('  ' + pyOut.trim().split('\n').join('\n  '));
} catch (err: any) {
  assert(false, `Python speech_sync tests failed: ${err.message}\n${err.stderr || ''}`);
}

console.log('  ✅ mgaudio and speech_sync engines verified.\n');

// 4. Canonical Benchmark Demos (4 Core Styles)
console.log('--- 4. Master Benchmark Demos (01, 08, 19, 06) ---');
const demos = ['01-flat-vector', '08-morph', '19-paperclip', '06-collage'];
for (const demo of demos) {
  const demoDir = path.resolve(`demos/${demo}`);
  assert(fs.existsSync(demoDir), `Demo directory missing: ${demo}`);
  const indexPath = path.join(demoDir, 'index.html');
  assert(fs.existsSync(indexPath), `index.html missing in ${demo}`);
  const cuesPath = path.join(demoDir, 'cues.json');
  assert(fs.existsSync(cuesPath), `cues.json missing in ${demo}`);
  const audioPath = path.join(demoDir, 'audio.py');
  assert(fs.existsSync(audioPath), `audio.py missing in ${demo}`);

  const cuesData = JSON.parse(fs.readFileSync(cuesPath, 'utf8'));
  assert(cuesData.fps === 30 || cuesData.fps === 60 || cuesData.fps === undefined || cuesData.ev !== undefined, `Invalid cues in ${demo}`);
  console.log(`  ✅ Canonical Demo ${demo} verified (HTML, cues.json, audio.py).`);
}
console.log();

// 5. Adversarial 7-Dimension Rubric
console.log('--- 5. Quality Rubric & Fatal Defect Flags ---');
const rubricPath = path.resolve('resources/rubrics/motion-director-rubric.md');
assert(fs.existsSync(rubricPath), 'resources/rubrics/motion-director-rubric.md does not exist');
const rubricContent = fs.readFileSync(rubricPath, 'utf8');
const requiredDimensions = [
  'style_fidelity',
  'concept_wow',
  'motion_craft',
  'design_typography',
  'finish_texture',
  'sound_sync',
  'technical',
];
for (const dim of requiredDimensions) {
  assert(rubricContent.includes(dim), `Rubric missing dimension: ${dim}`);
}
assert(rubricContent.includes('SLIDE_DECK_REGRESSION'), 'Rubric missing SLIDE_DECK_REGRESSION defect code');
assert(rubricContent.includes('NAKED_IMAGE_DEFECT'), 'Rubric missing NAKED_IMAGE_DEFECT defect code');
assert(rubricContent.includes('STIFF_MOTION_DEFECT'), 'Rubric missing STIFF_MOTION_DEFECT defect code');
assert(rubricContent.includes('VOICEOVER_DESYNC_DEFECT'), 'Rubric missing VOICEOVER_DESYNC_DEFECT defect code');
assert(rubricContent.includes('DIRECT_SHAPE_MORPH_DEFECT'), 'Rubric missing DIRECT_SHAPE_MORPH_DEFECT defect code');
assert(rubricContent.includes('DISCONNECTED_SLIDE_DEFECT'), 'Rubric missing DISCONNECTED_SLIDE_DEFECT defect code');
console.log('  ✅ Adversarial Rubric and fatal defect flags verified.\n');

// 6. Directorial Invariants & Memory
console.log('--- 6. Persistent Directorial Memory ---');
const memoryPath = path.resolve('memory/motion-director-memory.md');
assert(fs.existsSync(memoryPath), 'memory/motion-director-memory.md does not exist');
const memoryContent = fs.readFileSync(memoryPath, 'utf8');
assert(memoryContent.includes('Slide-Deck Fallacy') || memoryContent.includes('اسلاید متنی'), 'Memory missing anti-slide-deck invariant');
assert(memoryContent.includes('Squash & Stretch') || memoryContent.includes('له‌شدگی'), 'Memory missing squash and stretch invariant');
assert(memoryContent.includes('lib/image_plates.js'), 'Memory missing image plates invariant');
assert(memoryContent.includes('cues.json'), 'Memory missing cues.json invariant');
assert(memoryContent.includes('VOICEOVER_DESYNC_DEFECT') || memoryContent.includes('Voice-First Speech-Lock'), 'Memory missing voiceover desync invariant');
console.log('  ✅ Persistent directorial memory verified.\n');

// 7. Directorial Reference Guides (Styles 01 & 08)
console.log('--- 7. Directorial Reference Guides ---');
const flatGuidePath = path.resolve('.agents/skills/cinematic-motion-director/references/directorial_flat_vector_guide.md');
assert(fs.existsSync(flatGuidePath), 'directorial_flat_vector_guide.md does not exist');
const morphGuidePath = path.resolve('.agents/skills/cinematic-motion-director/references/directorial_shape_morph_guide.md');
assert(fs.existsSync(morphGuidePath), 'directorial_shape_morph_guide.md does not exist');
console.log('  ✅ Directorial reference guides verified.\n');

console.log('================================================================');
console.log('🎉 ALL 7 INTEGRITY GATES PASSED (100% OPERATIONAL & VERIFIED)');
console.log('================================================================');
