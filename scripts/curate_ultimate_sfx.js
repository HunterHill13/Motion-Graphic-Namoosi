const fs = require('fs');
const path = require('path');

const ULTIMATE_SFX_ROOT =
  'C:\\Users\\Hill\\Desktop\\MotionBro4\\750 Free Sound FX_for_AE_PP_by_videolancer\\Ultimate SFX';
const PUBLIC_ULTIMATE_DIR = path.resolve(__dirname, '../public/sfx/ultimate');
const SCHEMA_OUT = path.resolve(__dirname, '../schemas/ultimate_sfx_catalog.json');
const TS_CATALOG_OUT = path.resolve(__dirname, '../src/motion/audio/UltimateSfxCatalog.ts');

// Category metadata: semantic roles, subtle studio gain staging, and matching templates
const CATEGORY_META = {
  Simple: {
    role: 'soft_swish',
    description: 'Clean, airy, unobtrusive whooshes and gentle motion swishes',
    recommendedVolume: 0.08,
    maxVolume: 0.12,
    matchingThemes: ['ALL'],
  },
  Corporate: {
    role: 'clean_transition',
    description: 'Smooth, modern corporate & SaaS motion transitions and warm tonal swells',
    recommendedVolume: 0.08,
    maxVolume: 0.12,
    matchingThemes: ['BENTO_GRID_SAAS', 'CONTINUOUS_UI_MORPH', 'DARK_GRAPHITE_TECH'],
  },
  Cinematic: {
    role: 'cinematic_swell',
    description: 'Deep atmospheric transitions, gentle booms, and spatial camera travel cues',
    recommendedVolume: 0.09,
    maxVolume: 0.13,
    matchingThemes: ['DARK_GRAPHITE_TECH', 'QUANTUM_BIO_DEEP_Z', 'KINETIC_ARCHITECTURAL_TYPO'],
  },
  Ambient: {
    role: 'ambient_air',
    description: 'Ethereal spatial pads, deep-Z immersion drones, and soft air textures',
    recommendedVolume: 0.07,
    maxVolume: 0.10,
    matchingThemes: ['QUANTUM_BIO_DEEP_Z', 'CONTINUOUS_UI_MORPH', 'TECHNICAL_BLUEPRINT'],
  },
  Cyber: {
    role: 'cyber_telemetry',
    description: 'Futuristic data streams, HUD scans, and sci-fi blueprint schematics',
    recommendedVolume: 0.07,
    maxVolume: 0.11,
    matchingThemes: ['DARK_GRAPHITE_TECH', 'TECHNICAL_BLUEPRINT', 'FINTECH_TRADING'],
  },
  'Notifications and Buttons': {
    role: 'ui_pop_click',
    description: 'Subtle tactile UI pops, gentle chimes, and micro-interaction clicks',
    recommendedVolume: 0.06,
    maxVolume: 0.10,
    matchingThemes: ['ALL'],
  },
  Subdrop: {
    role: 'deep_subdrop',
    description: 'Low-frequency sub-bass drops for major act reveals and depth dives',
    recommendedVolume: 0.10,
    maxVolume: 0.14,
    matchingThemes: ['QUANTUM_BIO_DEEP_Z', 'DARK_GRAPHITE_TECH', 'KINETIC_ARCHITECTURAL_TYPO'],
  },
  Impact: {
    role: 'soft_impact',
    description: 'Grounded physical landings for heavy typographic and structural arrivals',
    recommendedVolume: 0.09,
    maxVolume: 0.13,
    matchingThemes: ['KINETIC_ARCHITECTURAL_TYPO', 'NEO_BRUTALIST', 'DARK_GRAPHITE_TECH'],
  },
  Stomp: {
    role: 'rhythmic_stomp',
    description: 'Percussive rhythmic accents for kinetic typography and Neo-Brutalist beats',
    recommendedVolume: 0.08,
    maxVolume: 0.12,
    matchingThemes: ['KINETIC_ARCHITECTURAL_TYPO', 'NEO_BRUTALIST'],
  },
  Glitch: {
    role: 'digital_glitch',
    description: 'Crisp digital micro-glitches and data morph artifacts',
    recommendedVolume: 0.06,
    maxVolume: 0.10,
    matchingThemes: ['DARK_GRAPHITE_TECH', 'TECHNICAL_BLUEPRINT', 'NEO_BRUTALIST'],
  },
  Cartoon: {
    role: 'playful_pop',
    description: 'Organic pops and tactile snaps suited for papercraft and playful elements',
    recommendedVolume: 0.07,
    maxVolume: 0.11,
    matchingThemes: ['STOP_MOTION_PAPER', 'NEO_BRUTALIST'],
  },
  Nature: {
    role: 'organic_texture',
    description: 'Natural organic breezes and tactile rustles for paper and bio themes',
    recommendedVolume: 0.07,
    maxVolume: 0.10,
    matchingThemes: ['STOP_MOTION_PAPER', 'QUANTUM_BIO_DEEP_Z'],
  },
  Live: {
    role: 'acoustic_foley',
    description: 'Real-world acoustic foley and subtle organic movement',
    recommendedVolume: 0.07,
    maxVolume: 0.11,
    matchingThemes: ['STOP_MOTION_PAPER', 'BENTO_GRID_SAAS'],
  },
  Game: {
    role: 'score_up',
    description: 'Positive level-up and metric achievement accents',
    recommendedVolume: 0.07,
    maxVolume: 0.11,
    matchingThemes: ['FINTECH_TRADING', 'BENTO_GRID_SAAS', 'NEO_BRUTALIST'],
  },
  Agressive: {
    role: 'high_energy_accent',
    description: 'High-contrast energetic transitions (use sparingly at very low volume)',
    recommendedVolume: 0.05,
    maxVolume: 0.09,
    matchingThemes: ['NEO_BRUTALIST'],
  },
  Rock: {
    role: 'energetic_hit',
    description: 'Organic drum/cymbal accents',
    recommendedVolume: 0.06,
    maxVolume: 0.10,
    matchingThemes: ['NEO_BRUTALIST', 'KINETIC_ARCHITECTURAL_TYPO'],
  },
  Strobe: {
    role: 'pulse_flutter',
    description: 'Rhythmic gating and fast pulse transitions',
    recommendedVolume: 0.06,
    maxVolume: 0.09,
    matchingThemes: ['DARK_GRAPHITE_TECH', 'FINTECH_TRADING'],
  },
};

// Curated starter pack to copy into public/sfx/ultimate/ (40 diverse files across categories)
const STARTER_SELECTION = [
  { category: 'Simple', indices: [1, 2, 3, 4, 5, 6] },
  { category: 'Corporate', indices: [1, 2, 3, 4, 5] },
  { category: 'Cinematic', indices: [1, 2, 3, 4] },
  { category: 'Notifications and Buttons', indices: [1, 2, 3, 4, 5, 6] },
  { category: 'Cyber', indices: [1, 2, 3, 4] },
  { category: 'Ambient', indices: [1, 2, 3] },
  { category: 'Subdrop', indices: [1, 2, 3] },
  { category: 'Impact', indices: [1, 2, 3] },
  { category: 'Stomp', indices: [1, 2] },
  { category: 'Glitch', indices: [1, 2] },
  { category: 'Nature', indices: [1, 2] },
  { category: 'Live', indices: [1, 2] },
  { category: 'Game', indices: [1, 2] },
];

function sanitizeSlug(str) {
  return str.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
}

function buildCatalogAndCopyStarter() {
  fs.mkdirSync(PUBLIC_ULTIMATE_DIR, { recursive: true });
  fs.mkdirSync(path.dirname(SCHEMA_OUT), { recursive: true });

  const catalogEntries = [];
  const copiedStarterFiles = [];

  if (!fs.existsSync(ULTIMATE_SFX_ROOT)) {
    console.error('Ultimate SFX folder not found at:', ULTIMATE_SFX_ROOT);
    process.exit(1);
  }

  const dirs = fs
    .readdirSync(ULTIMATE_SFX_ROOT, { withFileTypes: true })
    .filter((d) => d.isDirectory() && d.name !== '(Preview)');

  for (const dir of dirs) {
    const categoryName = dir.name;
    const catPath = path.join(ULTIMATE_SFX_ROOT, categoryName);
    const meta = CATEGORY_META[categoryName] || {
      role: 'general_sfx',
      description: 'General motion sound effect',
      recommendedVolume: 0.08,
      maxVolume: 0.12,
      matchingThemes: ['ALL'],
    };

    const files = fs
      .readdirSync(catPath)
      .filter((f) => f.endsWith('.wav') || f.endsWith('.mp3'))
      .sort((a, b) => {
        const numA = parseInt((a.match(/(\d+)/) || [0, 0])[1], 10);
        const numB = parseInt((b.match(/(\d+)/) || [0, 0])[1], 10);
        return numA - numB;
      });

    files.forEach((fileName) => {
      const numMatch = fileName.match(/(\d+)\.(wav|mp3)$/i);
      const indexNum = numMatch ? parseInt(numMatch[1], 10) : 1;
      const ext = path.extname(fileName).toLowerCase();
      const slug = `${sanitizeSlug(categoryName)}_${indexNum}${ext}`;
      const localRelPath = `sfx/ultimate/${slug}`;
      const fullSourcePath = path.join(catPath, fileName);

      // Check if part of starter selection
      const starterSpec = STARTER_SELECTION.find((s) => s.category === categoryName);
      const isPreCopied = starterSpec ? starterSpec.indices.includes(indexNum) : false;

      if (isPreCopied) {
        const destPath = path.join(PUBLIC_ULTIMATE_DIR, slug);
        fs.copyFileSync(fullSourcePath, destPath);
        copiedStarterFiles.push({
          id: `${sanitizeSlug(categoryName)}_${indexNum}`,
          category: categoryName,
          role: meta.role,
          publicPath: localRelPath,
          recommendedVolume: meta.recommendedVolume,
          maxVolume: meta.maxVolume,
          matchingThemes: meta.matchingThemes,
        });
      }

      catalogEntries.push({
        id: `${sanitizeSlug(categoryName)}_${indexNum}`,
        category: categoryName,
        index: indexNum,
        role: meta.role,
        description: meta.description,
        recommendedVolume: meta.recommendedVolume,
        maxVolume: meta.maxVolume,
        matchingThemes: meta.matchingThemes,
        sourcePath: fullSourcePath,
        publicPath: localRelPath,
        preCopiedInPublic: isPreCopied,
      });
    });
  }

  const fullCatalog = {
    version: '2.0.0',
    sourceRoot: ULTIMATE_SFX_ROOT,
    totalIndexedFiles: catalogEntries.length,
    totalPreCopiedStarterFiles: copiedStarterFiles.length,
    gainStagingPolicy: {
      voiceoverTargetVolume: 1.0,
      bgmBaseVolume: 0.14,
      bgmDuckedVolume: 0.06,
      sfxRecommendedRange: [0.06, 0.12],
      sfxHardCeiling: 0.14,
      antiRepetitionRule: 'NEVER repeat the exact same SFX file consecutively; rotate across distinct indices and categories.',
    },
    starterPack: copiedStarterFiles,
    catalog: catalogEntries,
  };

  fs.writeFileSync(SCHEMA_OUT, JSON.stringify(fullCatalog, null, 2), 'utf-8');

  // Generate TypeScript module for runtime access
  const tsContent = `// AUTO-GENERATED BY scripts/curate_ultimate_sfx.js
// DO NOT EDIT MANUALLY

export interface UltimateSfxEntry {
  id: string;
  category: string;
  role: string;
  publicPath: string;
  recommendedVolume: number;
  maxVolume: number;
  matchingThemes: string[];
}

export const SUBTLE_SFX_HARD_CEILING = 0.14;
export const SUBTLE_SFX_DEFAULT_VOLUME = 0.08;

export const ULTIMATE_SFX_STARTER_PACK: UltimateSfxEntry[] = ${JSON.stringify(
    copiedStarterFiles,
    null,
    2
  )};

/**
 * Selects a diverse, non-repeating sequence of subtle SFX files tailored to a template theme and cue role.
 */
export function selectVariedSfxPool(
  role: 'whoosh' | 'impact' | 'click' | 'riser' | 'chime' | 'ambient' | 'cyber' | 'subdrop',
  themeId: string = 'DARK_GRAPHITE_TECH'
): UltimateSfxEntry[] {
  const roleMap: Record<string, string[]> = {
    whoosh: ['soft_swish', 'clean_transition', 'organic_texture'],
    impact: ['soft_impact', 'rhythmic_stomp', 'deep_subdrop'],
    click: ['ui_pop_click', 'digital_glitch', 'score_up'],
    riser: ['cinematic_swell', 'ambient_air', 'cyber_telemetry'],
    chime: ['ui_pop_click', 'score_up'],
    ambient: ['ambient_air', 'organic_texture', 'acoustic_foley'],
    cyber: ['cyber_telemetry', 'digital_glitch'],
    subdrop: ['deep_subdrop', 'cinematic_swell'],
  };

  const targetRoles = roleMap[role] || ['soft_swish', 'clean_transition'];
  const matches = ULTIMATE_SFX_STARTER_PACK.filter((entry) =>
    targetRoles.includes(entry.role)
  );

  // Prioritize theme-matched entries first, then general entries
  const themePrioritized = matches.sort((a, b) => {
    const aTheme = a.matchingThemes.includes(themeId) ? 0 : 1;
    const bTheme = b.matchingThemes.includes(themeId) ? 0 : 1;
    return aTheme - bTheme;
  });

  return themePrioritized.length > 0 ? themePrioritized : ULTIMATE_SFX_STARTER_PACK;
}
`;

  fs.writeFileSync(TS_CATALOG_OUT, tsContent, 'utf-8');
  console.log(`✅ Indexed ${catalogEntries.length} Ultimate SFX files into ${SCHEMA_OUT}`);
  console.log(`✅ Copied ${copiedStarterFiles.length} starter SFX files into ${PUBLIC_ULTIMATE_DIR}`);
  console.log(`✅ Generated TypeScript catalog at ${TS_CATALOG_OUT}`);
}

// CLI mode: allow copying specific SFX IDs on demand by the SFX Curator Subagent
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === '--copy-id' && args[1]) {
    const catalog = JSON.parse(fs.readFileSync(SCHEMA_OUT, 'utf-8'));
    const requestedIds = args.slice(1);
    for (const reqId of requestedIds) {
      const found = catalog.catalog.find((e) => e.id === reqId);
      if (found && fs.existsSync(found.sourcePath)) {
        const dest = path.resolve(__dirname, '../public', found.publicPath);
        fs.mkdirSync(path.dirname(dest), { recursive: true });
        fs.copyFileSync(found.sourcePath, dest);
        console.log(`✅ Copied ${found.id} -> ${found.publicPath} (rec vol: ${found.recommendedVolume})`);
      } else {
        console.warn(`⚠️ SFX ID not found: ${reqId}`);
      }
    }
  } else {
    buildCatalogAndCopyStarter();
  }
}
