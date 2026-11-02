# Anti-Cliché Rules & Materiality Restraint

## Mandate: Eliminate AI Video Tells & False Premium

> **Core Philosophy**: A motion graphic feels authored when every element has a structural reason to exist. "Premium" is not frosted glass, glow, or 3D particles; premium is **restraint, precision, legible hierarchy, and motivated motion**.

---

## 1. Banned Visual Crutches (Automatic Critique Fails)

| Cliché Pattern | Symptoms | What It Signals | Required Fix |
|---|---|---|---|
| **Fake Premium / Glow Soup** | Heavy drop shadows, neon cyan/purple glows, blurred Gaussian orbs in background, frosted glass panels (`backdrop-filter: blur`). | Amateur AI trying to look "high tech" without understanding spatial composition. | Strip all glows and frosted glass. Use crisp matte surfaces, controlled tonal ramps of a single brand accent, and geometric negative space. |
| **Card Soup** | Every metric, paragraph, and headline is enclosed in a rounded rectangle card. | Dashboard designer syndrome. | Turn information into pure typography, lines, diagrams, or negative space. Keep cards only when representing real physical artifacts. |
| **Subtitle / Transcript Wallpaper** | Full voiceover sentence printed word-for-word on screen. | Subtitle maker, not motion graphic. | Show only the 1–4 key anchor words or numbers that carry the semantic weight of the beat. Let the voice deliver the sentence; let the graphic deliver the structure. |
| **Scale-Pop Loop** | Every element enters by scaling $0.8 \to 1.0$ with slight bounce. | Template monotony. | Vary the entrance mechanisms: use geometric unroll (`DotToLine`), mask reveal (`clipPath`), structural draw (`TypeOutlineFill`), or spatial handoff. |
| **Perpetual Floating / Unsettled Drift** | Elements constantly bob, rotate randomly, or drift without ever arriving. | Inability to create visual confidence. | Let elements arrive with physical weight and settle firmly. Holds should maintain subtle breathing ($1.00 \to 1.03$) or motivated camera motion, not aimless floating. |
| **Bounce Everywhere** | Mascots, serious institutional names, and medical data all bounce with high elasticity. | Accidental playfulness. | Damping must match subject matter. Scientific, institutional, and medical titles require dignified damping ($\ge 16$, zero wobble). Mascots alone may use playful springs. |
| **Unmotivated Camera Drift** | Camera continuously pans or tilts even when the scene content has not changed depth or scale. | Pretending motion is cinematic by jiggling the lens. | Lock the camera rig or use motivated slow-push ($1.00 \to 1.05$) toward the active focal point. Camera moves only when the story shifts focus. |
| **Double-Exposed Swaps** | Incoming text or graphic appears while the outgoing element is still fading or lifting. | Muddy compositing defect. | Outgoing element must be 100% gone before incoming lands (Sequential Swap Rule). |

---

## 2. "Add Shape, Not Word" Principle

The Agent may freely invent:
- Geometric anchors, lines, grids, dividing vectors
- Masking boundaries, expanding thresholds
- Depth parallax and camera framing
- Physical reactions, collisions, shockwaves
- Abstract visual metaphors (e.g. scattered points collating into a cluster)

The Agent may **NEVER** invent:
- Fictitious numbers, percentages, or dates
- English buzzwords ("AI Powered", "Seamless", "Next-Gen") unless in source
- Unverified medical or scientific claims
- Unauthorized institutional labels or logos

---

## 3. "Diagnose Before Decorating" Ladder

When an animation feels flat, weak, or clumsy, work top-down through this leverage hierarchy:

1. **Check Enter & Exit Timing**: Are elements blinking in? Are exits abrupt? Fix the arrival curve first.
2. **Check Non-Robotic Physics**: Is motion linear? Replace linear interpolation with spring physics or cubic bezier (`[0.16, 1, 0.3, 1]`).
3. **Check Stagger**: Are multiple elements arriving at the exact same frame? Offset them 3–5 frames apart.
4. **Check Hierarchy & Focal Point**: Does the viewer know where to look first? Demote secondary elements.
5. **Check Readability**: Is text legible at 360px phone width? Clamped against clipping?
6. **NEVER** add particles, glows, or extra motion to mask a timing defect!
