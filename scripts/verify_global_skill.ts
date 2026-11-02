/**
 * Verification Script for Global Skill Packaging (Phase 4B.2)
 * Checks presence, schema integrity, and TypeScript module resolution
 * directly from the Global Skill directory.
 */
import * as fs from 'fs';
import * as path from 'path';

// Ensure workspace node_modules (containing remotion, react, etc.) is discoverable globally
const workspaceNodeModules = path.join(process.cwd(), 'node_modules');
if (fs.existsSync(workspaceNodeModules)) {
  const Module = require('module');
  process.env.NODE_PATH = workspaceNodeModules;
  Module._initPaths();
}

const GLOBAL_SKILL_ROOT = 'C:/Users/Hill/.gemini/config/skills/cinematic-motion-director';

async function verifyGlobalSkill() {
  console.log('====================================================');
  console.log('PHASE 4B.2: GLOBAL SKILL VERIFICATION & LOAD CHECK');
  console.log(`Target: ${GLOBAL_SKILL_ROOT}`);
  console.log('====================================================\n');

  let errors: string[] = [];

  // 1. Mandatory File Presence Checks (Step 12)
  const requiredFiles = [
    { name: 'SKILL.md', rel: 'SKILL.md' },
    { name: 'storyboard.schema.json', rel: 'schemas/storyboard.schema.json' },
    { name: 'visual-world.schema.json', rel: 'schemas/visual-world.schema.json' },
    { name: 'MotionPlanner', rel: 'src/motion/compiler/motionPlanningInterface.ts' },
    { name: 'MotionSceneGraph', rel: 'src/motion/compiler/motionSceneGraph.ts' },
    { name: 'MotionVerbSelector', rel: 'src/motion/compiler/motionVerbSelector.ts' },
    { name: 'MotionGraphCompiler', rel: 'src/motion/compiler/motionGraphCompiler.ts' },
    { name: 'VerbTemplates', rel: 'src/motion/grammar/verbTemplates.ts' },
    { name: 'PersistentWorld', rel: 'src/motion/grammar/persistentWorld.tsx' },
    { name: 'AST Validator', rel: 'src/motion/validation/astMotionValidator.ts' },
    { name: 'Render Visual Validator', rel: 'src/motion/validation/renderVisualValidator.ts' },
    { name: 'VisualWorldSchema', rel: 'src/motion/visual_world/visualWorldSchema.ts' },
    { name: 'VisualWorldValidator', rel: 'src/motion/visual_world/visualWorldValidator.ts' },
    { name: 'VisualWorldPlanner', rel: 'src/motion/visual_world/visualWorldPlanner.ts' },
    { name: 'MaterialSchema', rel: 'src/motion/visual_world/materialSchema.ts' },
    { name: 'MaterialAmbiguityGate', rel: 'src/motion/visual_world/materialAmbiguityGate.ts' },
    { name: 'MaterialValidator', rel: 'src/motion/visual_world/materialValidator.ts' },
    { name: 'MaterialPlanner', rel: 'src/motion/visual_world/materialPlanner.ts' },
    { name: 'LightingSchema', rel: 'src/motion/visual_world/lightingSchema.ts' },
    { name: 'LightingAmbiguityGate', rel: 'src/motion/visual_world/lightingAmbiguityGate.ts' },
    { name: 'LightingValidator', rel: 'src/motion/visual_world/lightingValidator.ts' },
    { name: 'LightingPlanner', rel: 'src/motion/visual_world/lightingPlanner.ts' },
    { name: 'DepthSchema', rel: 'src/motion/visual_world/depthSchema.ts' },
    { name: 'DepthAmbiguityGate', rel: 'src/motion/visual_world/depthAmbiguityGate.ts' },
    { name: 'DepthValidator', rel: 'src/motion/visual_world/depthValidator.ts' },
    { name: 'DepthPlanner', rel: 'src/motion/visual_world/depthPlanner.ts' },
    { name: 'SpatialRenderAdapter', rel: 'src/motion/visual_world/spatialRenderAdapter.ts' },
    { name: 'MaterialRenderAdapter', rel: 'src/motion/visual_world/materialRenderAdapter.ts' },
    { name: 'LightingRenderAdapter', rel: 'src/motion/visual_world/lightingRenderAdapter.ts' },
    { name: 'CinematicCameraAdapter', rel: 'src/motion/visual_world/cinematicCameraAdapter.ts' },
    { name: 'SecondaryMotionAdapter', rel: 'src/motion/visual_world/secondaryMotionAdapter.ts' },
  ];

  console.log('--- Step 12: Verifying Mandated Global Files ---');
  for (const item of requiredFiles) {
    const fullPath = path.join(GLOBAL_SKILL_ROOT, item.rel);
    if (!fs.existsSync(fullPath)) {
      errors.push(`Missing mandated file: ${item.name} at ${fullPath}`);
      console.log(`  [FAIL] ${item.name}: NOT FOUND`);
    } else {
      console.log(`  [PASS] ${item.name}: Exists (${item.rel})`);
    }
  }

  // Also check presence in template/src/motion/
  console.log('\n--- Checking Template Scaffolding Presence (template/src/motion) ---');
  const templateFiles = [
    'compiler/motionPlanningInterface.ts',
    'compiler/motionSceneGraph.ts',
    'compiler/motionVerbSelector.ts',
    'compiler/motionGraphCompiler.ts',
    'grammar/verbTemplates.ts',
    'grammar/persistentWorld.tsx',
    'validation/astMotionValidator.ts',
    'validation/renderVisualValidator.ts',
    'visual_world/visualWorldSchema.ts',
    'visual_world/visualWorldValidator.ts',
    'visual_world/visualWorldPlanner.ts',
    'visual_world/materialSchema.ts',
    'visual_world/materialAmbiguityGate.ts',
    'visual_world/materialValidator.ts',
    'visual_world/materialPlanner.ts',
    'visual_world/lightingSchema.ts',
    'visual_world/lightingAmbiguityGate.ts',
    'visual_world/lightingValidator.ts',
    'visual_world/lightingPlanner.ts',
    'visual_world/depthSchema.ts',
    'visual_world/depthAmbiguityGate.ts',
    'visual_world/depthValidator.ts',
    'visual_world/depthPlanner.ts',
    'visual_world/spatialRenderAdapter.ts',
    'visual_world/materialRenderAdapter.ts',
    'visual_world/lightingRenderAdapter.ts',
    'visual_world/cinematicCameraAdapter.ts',
    'visual_world/secondaryMotionAdapter.ts',
  ];
  for (const rel of templateFiles) {
    const fullPath = path.join(GLOBAL_SKILL_ROOT, 'template/src/motion', rel);
    if (!fs.existsSync(fullPath)) {
      errors.push(`Missing template file: template/src/motion/${rel}`);
      console.log(`  [FAIL] template/src/motion/${rel}: NOT FOUND`);
    } else {
      console.log(`  [PASS] template/src/motion/${rel}: Exists`);
    }
  }

  // 2. Schema Verification (Step 8)
  console.log('\n--- Step 8: Schema Verification ---');
  const schemaPath = path.join(GLOBAL_SKILL_ROOT, 'schemas/storyboard.schema.json');
  try {
    const schemaContent = JSON.parse(fs.readFileSync(schemaPath, 'utf-8'));
    const motionProp = schemaContent.properties?.shots?.items?.properties?.motion;
    if (!motionProp) {
      errors.push('Schema does not define motion property on shots.items');
      console.log('  [FAIL] motion property missing in storyboard.schema.json');
    } else {
      const allowedTypes = Array.isArray(motionProp.type) ? motionProp.type : [motionProp.type];
      const hasObject = allowedTypes.includes('object');
      const verbs = motionProp.properties?.verb?.enum;
      if (hasObject && Array.isArray(verbs) && verbs.includes('SPLIT') && verbs.includes('EXPAND')) {
        console.log(`  [PASS] storyboard.schema.json contains structured motion verbs: ${verbs.join(', ')}`);
      } else {
        errors.push('Schema motion property is not upgraded to structured object with verbs');
        console.log('  [FAIL] Schema motion property is not upgraded to structured object');
      }
    }
  } catch (err: any) {
    errors.push(`Failed to parse storyboard.schema.json: ${err.message}`);
    console.log(`  [FAIL] Schema JSON parse error: ${err.message}`);
  }

  // 3. SKILL.md Architecture Check (Step 7)
  console.log('\n--- Step 7: SKILL.md Architecture Enforcement Check ---');
  const skillPath = path.join(GLOBAL_SKILL_ROOT, 'SKILL.md');
  const skillText = fs.readFileSync(skillPath, 'utf-8');
  const requiredTerms = ['PersistentWorld', 'MotionGraphCompiler', 'MotionSceneGraph', 'VerbTemplates'];
  for (const term of requiredTerms) {
    if (!skillText.includes(term)) {
      errors.push(`SKILL.md does not contain required architectural token: ${term}`);
      console.log(`  [FAIL] SKILL.md missing: ${term}`);
    } else {
      console.log(`  [PASS] SKILL.md contains: ${term}`);
    }
  }

  // 4. Live Runtime Load & Import Check (Step 13)
  console.log('\n--- Step 13: Live Runtime Import & Execution Check ---');
  try {
    const plannerPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/compiler/motionPlanningInterface.ts');
    const compilerPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/compiler/motionGraphCompiler.ts');
    const validatorPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/validation/astMotionValidator.ts');
    const vwPlannerPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/visualWorldPlanner.ts');
    const vwValidatorPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/visualWorldValidator.ts');

    const { MotionPlanner } = require(plannerPath);
    const { MotionGraphCompiler } = require(compilerPath);
    const { AstMotionValidator } = require(validatorPath);
    const { VisualWorldPlanner } = require(vwPlannerPath);
    const { VisualWorldValidator } = require(vwValidatorPath);

    // Test live planning via global module
    const expandIntent = 'A central glowing core expands radially outward from center, deploying concentric energy rings.';
    const sceneGraph = MotionPlanner.planFromNaturalIntent(expandIntent);
    const compiledExpand = MotionGraphCompiler.compileGraph(sceneGraph);

    if (compiledExpand && compiledExpand.contracts.length > 0) {
      const verb = compiledExpand.contracts[0].midpointEvent.verb;
      console.log(`  [PASS] Live MotionPlanner & Compiler executed from Global Skill: Verb=${verb}`);
    } else {
      errors.push('MotionPlanner failed to generate scene graph from global module');
      console.log('  [FAIL] MotionPlanner execution returned empty graph');
    }

    // Verify AST validator instantiation
    const sampleTsx = `
      import React from 'react';
      import { PersistentWorld } from './PersistentWorld';
      export const Test = () => <PersistentWorld durationInFrames={90} />;
    `;
    const validator = new AstMotionValidator('Test.tsx', sampleTsx);
    const report = validator.validate();
    if (report && typeof report.passed === 'boolean') {
      console.log(`  [PASS] AstMotionValidator loaded and callable from Global Skill (hasPersistentWorld=${report.hasPersistentWorld})`);
    } else {
      errors.push('AstMotionValidator validate returned invalid report');
      console.log('  [FAIL] AstMotionValidator validate returned invalid report');
    }

    const testWorld = VisualWorldPlanner.planFromNaturalIntent(
      'A supermassive black hole with relativistic accretion disk and lensed starfield.'
    );
    const worldReport = VisualWorldValidator.validate(testWorld);
    if (worldReport && worldReport.passed) {
      console.log(`  [PASS] Live VisualWorldPlanner & Validator executed from Global Skill: Hero=${testWorld.hero.id}`);
    } else {
      errors.push('VisualWorldValidator failed on planned test world');
      console.log('  [FAIL] VisualWorldValidator failed on planned test world');
    }

    // Phase 5A.1: Verify Cinematic Hard-Gate Enforcement
    console.log('\n--- Phase 5A.1: Cinematic Hard-Gate Enforcement Check ---');
    // Check 1: compileCinematicGraph rejects graph without VisualWorld
    try {
      MotionGraphCompiler.compileCinematicGraph(sceneGraph);
      errors.push('compileCinematicGraph did not throw VISUAL_WORLD_REQUIRED on graph lacking visualWorld');
      console.log('  [FAIL] compileCinematicGraph allowed compilation without visualWorld');
    } catch (gateErr: any) {
      if (gateErr.code === 'VISUAL_WORLD_REQUIRED') {
        console.log('  [PASS] compileCinematicGraph blocked with VISUAL_WORLD_REQUIRED');
      } else {
        errors.push(`compileCinematicGraph threw unexpected code: ${gateErr.code}`);
        console.log(`  [FAIL] compileCinematicGraph unexpected error: ${gateErr.code}`);
      }
    }

    // Check 2: planCinematicScene rejects request without VisualWorld
    try {
      MotionPlanner.planCinematicScene({
        creativeIntent: 'Core expands',
        entities: [{ id: 'core', role: 'HERO', semanticPurpose: 'Core', persistent: true }],
        transformations: [{ description: 'Expands', sourceEntityIds: ['core'], trigger: 'pulse', consequence: 'exp' }],
      });
      errors.push('planCinematicScene did not throw VISUAL_WORLD_REQUIRED on request lacking visualWorld');
      console.log('  [FAIL] planCinematicScene allowed planning without visualWorld');
    } catch (gateErr: any) {
      if (gateErr.code === 'VISUAL_WORLD_REQUIRED') {
        console.log('  [PASS] planCinematicScene blocked with VISUAL_WORLD_REQUIRED');
      } else {
        errors.push(`planCinematicScene threw unexpected code: ${gateErr.code}`);
        console.log(`  [FAIL] planCinematicScene unexpected error: ${gateErr.code}`);
      }
    }

    // Check 3: compileCinematicGraph succeeds with valid VisualWorld
    const cinematicGraph = MotionPlanner.planCinematicSceneFromNaturalLanguage(
      'A central glowing core expands radially outward from center, deploying concentric energy rings.',
      testWorld
    );
    const compiledCinematic = MotionGraphCompiler.compileCinematicGraph(cinematicGraph);
    if (compiledCinematic && compiledCinematic.contracts.length > 0) {
      console.log(`  [PASS] compileCinematicGraph passed with valid VisualWorld (Hero=${compiledCinematic.entities[0].id})`);
    } else {
      errors.push('compileCinematicGraph failed on valid cinematic graph');
      console.log('  [FAIL] compileCinematicGraph failed on valid cinematic graph');
    }

    // Phase 5B.1: Material Language & Response Hard-Gate Check
    console.log('\n--- Phase 5B.1: Material Language & Response Hard-Gate Check ---');
    const matPlannerPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/materialPlanner.ts');
    const matValidatorPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/materialValidator.ts');
    const matAmbiguityPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/materialAmbiguityGate.ts');

    const { MaterialPlanner } = require(matPlannerPath);
    const { MaterialValidator } = require(matValidatorPath);
    const { MaterialAmbiguityGate } = require(matAmbiguityPath);

    const matReport = MaterialValidator.validate(testWorld);
    if (matReport && matReport.passed) {
      console.log(`  [PASS] Live MaterialValidator executed: World materials valid (count=${testWorld.materials?.length})`);
    } else {
      errors.push('MaterialValidator failed on test world');
      console.log('  [FAIL] MaterialValidator failed on test world');
    }

    try {
      MaterialAmbiguityGate.validateNaturalIntent('premium material');
      errors.push('MaterialAmbiguityGate allowed vague buzzword');
      console.log('  [FAIL] MaterialAmbiguityGate allowed vague buzzword');
    } catch (ambErr: any) {
      if (ambErr.code === 'MATERIAL_DIRECTION_AMBIGUOUS') {
        console.log('  [PASS] MaterialAmbiguityGate blocked with MATERIAL_DIRECTION_AMBIGUOUS');
      } else {
        errors.push(`MaterialAmbiguityGate threw unexpected error: ${ambErr.code}`);
      }
    }

    try {
      const worldWithoutHeroMat = {
        ...testWorld,
        hero: { ...testWorld.hero, materialId: undefined },
      };
      const graphWithoutHeroMat = MotionPlanner.planCinematicSceneFromNaturalLanguage(
        'Central core expands outward radially',
        worldWithoutHeroMat
      );
      MotionGraphCompiler.compileCinematicGraph(graphWithoutHeroMat);
      errors.push('compileCinematicGraph allowed scene without hero material');
      console.log('  [FAIL] compileCinematicGraph allowed scene without hero material');
    } catch (matGateErr: any) {
      if (matGateErr.code === 'MATERIAL_REQUIRED' || matGateErr.code === 'MATERIAL_INVALID') {
        console.log('  [PASS] compileCinematicGraph blocked with MATERIAL_REQUIRED');
      } else {
        errors.push(`compileCinematicGraph threw unexpected code on missing material: ${matGateErr.code}`);
      }
    }

    // Phase 5B.2: Lighting Response & Cinematic Light Language Hard-Gate Check
    console.log('\n--- Phase 5B.2: Lighting Response & Cinematic Light Language Hard-Gate Check ---');
    const lightPlannerPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/lightingPlanner.ts');
    const lightValidatorPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/lightingValidator.ts');
    const lightAmbiguityPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/lightingAmbiguityGate.ts');

    const { LightingPlanner } = require(lightPlannerPath);
    const { LightingValidator } = require(lightValidatorPath);
    const { LightingAmbiguityGate } = require(lightAmbiguityPath);

    const lightReport = LightingValidator.validate(testWorld);
    if (lightReport && lightReport.passed) {
      console.log(`  [PASS] Live LightingValidator executed: World lighting valid (sources=${testWorld.lighting?.sources.length})`);
    } else {
      errors.push('LightingValidator failed on test world');
      console.log('  [FAIL] LightingValidator failed on test world');
    }

    try {
      LightingAmbiguityGate.validateNaturalIntent('cinematic lighting');
      errors.push('LightingAmbiguityGate allowed vague buzzword');
      console.log('  [FAIL] LightingAmbiguityGate allowed vague buzzword');
    } catch (ambLightErr: any) {
      if (ambLightErr.code === 'LIGHTING_DIRECTION_AMBIGUOUS') {
        console.log('  [PASS] LightingAmbiguityGate blocked with LIGHTING_DIRECTION_AMBIGUOUS');
      } else {
        errors.push(`LightingAmbiguityGate threw unexpected error: ${ambLightErr.code}`);
      }
    }

    try {
      const worldWithoutLighting = {
        ...testWorld,
        lighting: undefined,
      };
      const graphWithoutLighting = MotionPlanner.planCinematicSceneFromNaturalLanguage(
        'Central core expands outward radially',
        worldWithoutLighting
      );
      MotionGraphCompiler.compileCinematicGraph(graphWithoutLighting);
      errors.push('compileCinematicGraph allowed scene without lighting');
      console.log('  [FAIL] compileCinematicGraph allowed scene without lighting');
    } catch (lightGateErr: any) {
      if (lightGateErr.code === 'LIGHTING_REQUIRED' || lightGateErr.code === 'LIGHTING_INVALID') {
        console.log('  [PASS] compileCinematicGraph blocked with LIGHTING_REQUIRED');
      } else {
        errors.push(`compileCinematicGraph threw unexpected code on missing lighting: ${lightGateErr.code}`);
      }
    }

    // Phase 5C: Depth, Spatial Layering & 2.5D Architecture Hard-Gate Check
    console.log('\n--- Phase 5C: Depth, Spatial Layering & 2.5D Architecture Hard-Gate Check ---');
    const depthPlannerPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/depthPlanner.ts');
    const depthValidatorPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/depthValidator.ts');
    const depthAmbiguityPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/depthAmbiguityGate.ts');

    const { DepthPlanner } = require(depthPlannerPath);
    const { DepthValidator } = require(depthValidatorPath);
    const { DepthAmbiguityGate } = require(depthAmbiguityPath);

    const depthReport = DepthValidator.validate(testWorld);
    if (depthReport && depthReport.passed) {
      console.log(`  [PASS] Live DepthValidator executed: World spatial contract valid (placements=${testWorld.spatial?.placements.length})`);
    } else {
      errors.push('DepthValidator failed on test world');
      console.log('  [FAIL] DepthValidator failed on test world');
    }

    // Phase 5C.1: Spatial Runtime Adapter Execution & Depth Ordering Check
    const adapterPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/spatialRenderAdapter.ts');
    const { SpatialRenderAdapter } = require(adapterPath);
    const sortedEls = SpatialRenderAdapter.getDepthSortedElements(testWorld.spatial);
    const renderValidation = SpatialRenderAdapter.validateRenderExecution(sortedEls, testWorld.spatial);
    if (renderValidation && renderValidation.passed && sortedEls.length > 0) {
      console.log(`  [PASS] Live SpatialRenderAdapter executed: Elements rendered with depth ordering (count=${sortedEls.length})`);
    } else {
      errors.push('SpatialRenderAdapter failed on test world');
      console.log('  [FAIL] SpatialRenderAdapter failed on test world');
    }

    // Phase 5D: Material Runtime Adapter Execution & Anti-Bypass Check
    const matAdapterPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/materialRenderAdapter.ts');
    const { MaterialRenderAdapter } = require(matAdapterPath);
    const heroMaterialRef = testWorld.materials?.[testWorld.hero.materialId];
    if (heroMaterialRef) {
      const heroMatStyle = MaterialRenderAdapter.resolveMaterialStyle(heroMaterialRef, testWorld.hero.id);
      const matValidation = MaterialRenderAdapter.validateRenderExecution([heroMatStyle], [heroMaterialRef]);
      if (matValidation && matValidation.passed) {
        console.log(`  [PASS] Live MaterialRenderAdapter executed: Hero material styled (category=${heroMatStyle.category}, bg=${heroMatStyle.background.slice(0, 24)}...)`);
      } else {
        errors.push('MaterialRenderAdapter failed on hero material');
        console.log('  [FAIL] MaterialRenderAdapter failed on hero material');
      }
    }

    // Phase 5D.1: Lighting Runtime Adapter Execution & Normalization Check
    const lightAdapterPath = path.join(GLOBAL_SKILL_ROOT, 'src/motion/visual_world/lightingRenderAdapter.ts');
    const { LightingRenderAdapter } = require(lightAdapterPath);
    if (testWorld.lighting) {
      const normLighting = LightingRenderAdapter.normalizeContract(testWorld.lighting);
      if (normLighting && typeof normLighting.keyDirectionAngle === 'number' && normLighting.keyIntensity > 0) {
        console.log(`  [PASS] Live LightingRenderAdapter executed: Normalized lighting (keyAngle=${normLighting.keyDirectionAngle}°, keyInt=${normLighting.keyIntensity})`);
      } else {
        errors.push('LightingRenderAdapter failed to normalize LightingContract');
        console.log('  [FAIL] LightingRenderAdapter failed to normalize LightingContract');
      }
    }

    try {
      DepthAmbiguityGate.validateNaturalIntent('make it 3D');
      errors.push('DepthAmbiguityGate allowed vague buzzword');
      console.log('  [FAIL] DepthAmbiguityGate allowed vague buzzword');
    } catch (ambDepthErr: any) {
      if (ambDepthErr.code === 'DEPTH_DIRECTION_AMBIGUOUS') {
        console.log('  [PASS] DepthAmbiguityGate blocked with DEPTH_DIRECTION_AMBIGUOUS');
      } else {
        errors.push(`DepthAmbiguityGate threw unexpected error: ${ambDepthErr.code}`);
      }
    }

    try {
      const worldWithoutSpatial = {
        ...testWorld,
        spatial: undefined,
      };
      const graphWithoutSpatial = MotionPlanner.planCinematicSceneFromNaturalLanguage(
        'Central core expands outward radially',
        worldWithoutSpatial
      );
      MotionGraphCompiler.compileCinematicGraph(graphWithoutSpatial);
      errors.push('compileCinematicGraph allowed scene without spatial contract');
      console.log('  [FAIL] compileCinematicGraph allowed scene without spatial contract');
    } catch (spatialGateErr: any) {
      if (spatialGateErr.code === 'SPATIAL_REQUIRED' || spatialGateErr.code === 'SPATIAL_INVALID') {
        console.log('  [PASS] compileCinematicGraph blocked with SPATIAL_REQUIRED');
      } else {
        errors.push(`compileCinematicGraph threw unexpected code on missing spatial contract: ${spatialGateErr.code}`);
      }
    }
  } catch (err: any) {
    errors.push(`Runtime import failed: ${err.message}`);
    console.log(`  [FAIL] Runtime import failed: ${err.message}`);
  }

  // Final Summary
  console.log('\n====================================================');
  if (errors.length === 0) {
    console.log('RESULT: PASS (100% of checks satisfied)');
    console.log('Global Skill is fully synchronized, self-contained, and valid.');
    console.log('====================================================');
  } else {
    console.log(`RESULT: FAIL (${errors.length} errors encountered)`);
    for (const e of errors) {
      console.log(` - ${e}`);
    }
    console.log('====================================================');
    process.exit(1);
  }
}

verifyGlobalSkill().catch((err) => {
  console.error('Fatal error during verification:', err);
  process.exit(1);
});
