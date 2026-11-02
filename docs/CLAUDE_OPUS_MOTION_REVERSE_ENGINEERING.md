# Claude Opus 5.5 Motion Graphics: Deep Reverse-Engineering & Architecture Report

**Author:** Antigravity AI Engineering Team  
**Date:** October 2026  
**Sources Investigated:**
- `https://www.ai.joaoqueiros.com/blog/opus-5-5-video-motion-examples-prompts` (João Queirós, JQ AI Systems)
- `https://github.com/yihui-dev/awesome-opus5-5-videos` (513 curated prompts & Skillry live remakes)
- `https://www.ayautomate.com/resources/claude-opus-5-5-motion-graphics` (AY Automate LLC, 48 X posts analysis)
- `https://youmind.com/opus-5-5-prompts` (YouMind HTML Video & Animation library)
- `https://github.com/remotion-dev/skills` (Official Remotion Agent Skills for Claude Code)
- `https://github.com/Vincentwei1021/video-shotcraft` & `video-talkcraft` (Vincent Wei's 157-recipe motion skills)

---

## 1. Executive Summary & Reality Check: What is "Claude Opus 5.5 Motion"?

In late September and October 2026, a viral phenomenon swept X (Twitter), YouTube, and GitHub showcasing stunning motion graphics videos allegedly produced by "Claude Opus 5.5". 

Our primary-source reverse engineering reveals the precise reality:

1. **The Core Mechanism:**
   "Opus 5.5" does not render video pixels via a generative diffusion model like Sora, Kling, or Runway. Instead, **Claude writes executable animation code** (React/Remotion, HTML5 Canvas, SVG with GSAP, or Three.js WebGL shaders) which is then executed in a browser or Remotion runtime and exported to MP4.
2. **Zero Hallucination, Crisp 60 FPS Vector Precision:**
   Because the video is generated through deterministic code, texts are razor-sharp, geometries never warp or blur, brand logos stay identical, and timings are mathematically locked to audio beats.
3. **The Famous "Showreel" Prompt Trigger:**
   Over 60% of the viral videos used variants of a single psychological trigger prompt:
   > *"Make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. Go all out."*
   When given this prompt, Claude assumes the persona of a world-class motion designer and outputs complex, multi-layered visual compositions.

---

## 2. Anatomical Deconstruction of Viral Creator Prompts

From our analysis of `yihui-dev/awesome-opus5-5-videos` (513 prompts) and creator workflows (Samson Vowles / Delightful Design, @twoclipping, @himanshutwtxs, @moritzkremb, @anabology):

### A. The Structural Formula of Elite Prompts
The most successful creators did NOT use vague prompts. They used XML-tagged structured briefs:

```xml
<inputs>
Specify 8–12 UI states, exact brand colors, 120 BPM audio track.
</inputs>

<direction>
Dribbble-level UI motion. One shape, never cut: every state is the same element 
morphing its size, radius, and color while content swaps with a short blur.
Springs everywhere, tiny overshoot at most. 
Banned: bouncy easing, particle bursts, mismatched icon strokes, dead time.
</direction>

<structure>
120 BPM, 7 bars, something happens on every beat:
Button → loader → check → dynamic island → music player → volume slider → 
liquid tab indicator → self-drawing chart → command palette → toast.
</structure>

<build>
1. Every style is computed from time inside seek(t): no CSS transitions, no timers.
2. Springs are closed-form step responses (pure function of time).
3. The tab indicator's two edges ride different springs (leading edge stretches).
4. Direct manipulation cursor physics.
5. Render with Playwright/Remotion: subframe motion blur at 60fps.
</build>

<gotchas>
Never put will-change on anything the camera scales (prevents blur). 
Text swapping inside morphing containers needs separate enter/exit timing.
</gotchas>
```

### B. The 5 Cardinal Technical Commandments
1. **Never use CSS `transition` or `animation`**: In video rendering, the timeline must be completely scrubbable (`seek(t)` or `useCurrentFrame()`). CSS transitions fail during headless frame export.
2. **Spring Physics over Cubic Bezier**: High-end motion design uses physical springs (`damping: 14–20, stiffness: 120–180, mass: 0.8`), not bouncy cartoon easing.
3. **Staggered Delays**: Pop-in events are staggered by 3–6 frames (e.g., card background at frame 0, icon badge at frame 4, headline at frame 8, metrics at frame 14).
4. **Continuous Micro-Life (Sub-Motion)**: Even during informational "rest" periods, background bokeh floats, conduits pulse with traveling light packets, and glow highlights gently breathe.
5. **Frame Budget for Reading**: Every major graphic transformation must hold for $\ge 1.0\text{s}$ (30–45 frames) to allow human comprehension before the next transition.

---

## 3. Reverse Engineering the Skills: How Anthropic & Community Implement It

### A. Official `remotion-dev/skills` (By Remotion Team)
Remotion published official agent skills for Claude Code (`@remotion/skills`):
- **`remotion-markup`**: Teaches Claude the exact rules of React-based video rendering:
  - Use `interpolate(frame, [in], [out], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.spring() })`.
  - Use transform shorthands (`scale`, `translate`, `rotate`) rather than monolithic `transform` strings so the Remotion Studio visual editor can inspect and modify properties.
  - Wrap components in `<Interactive.withSchema()>` to expose live controls to the user.
  - Use `premountFor={fps}` on all `<Sequence>` and media components to pre-cache frames and eliminate stutter.

### B. `video-shotcraft` & `video-talkcraft` (By Vincent Wei)
The most sophisticated Claude Code skills in the wild:
- **157 Shot Recipe Cards**: Pre-engineered motion recipes (`deck-deal-flyin`, `spotlight-hero-card`, `row-embed`, `evidence-scroll-tour`, `magnifier-detail`, etc.).
- **7-Layer Anti-Slideshow Camera**:
  1. Base canvas (dark theme with subtle radial gradient)
  2. Structural panels & frosted glass cards
  3. Interactive graphics & data telemetry
  4. Typography & callouts
  5. Ambient floating particles & glow highlights
  6. Camera tracking & motivated 2.5D push-in (`1.00 → 1.05`)
  7. Audio-synchronized SFX (riser → impact → sparkle)
- **Word-Level Narration Alignment**: Synchronizing visual triggers to speech timestamps (`tSay/msSay`) within 20–40ms precision.

---

## 4. Root Cause Analysis: Why Our Previous Phases (5A–5F) Had a Quality Gap

| Dimension | Previous Compiler Architecture (Phases 5A–5F) | Claude Opus 5.5 / Claude Motion Paradigm |
|---|---|---|
| **Objective Function** | Optimize for passing 15+ AST mathematical validator gates | Optimize for human visual appeal, contrast, and rhythm |
| **Motion Vocabulary** | Dogmatically restricted to 8 abstract verbs (`SPLIT`, `EXPAND`, etc.) | Rich visual recipes (Glass cards, conduits, donut gauges, word-by-word staggered kinetic typography) |
| **Styling** | Primitive SVG vector paths and flat boxes | Glassmorphism (`backdropFilter: blur(18px)`), radial volumetric lighting, specular edge highlights, multi-stop linear gradients |
| **Camera** | Mathematical coordinate verification ($z \in [0, 1]$) | Motivated cinematography: subtle continuous 2.5D push-in, parallax depth planes, rest/hold budgets |
| **Feedback Loop** | Headless unit tests checking AST trees | Visual contact sheets, frame inspection, and iterative visual refinement |

---

## 5. Strategic Roadmap: Integrating Claude Motion Excellence into Our Skill

To bring our `cinematic-motion-director` skill to full parity with Claude Opus 5.5:

```text
                                [USER PROMPT]
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
     [A: SHOWREEL / DEMO MODE]                      [B: PERSIAN EXPLAINER MODE]
  "Make a dynamic 15s showreel..."              "ویدیو معرفی با صدای کاوه..."
              │                                               │
              ├───────────────────────┬───────────────────────┤
                                      ▼
                      [CLAUDE MOTION RECIPE STUDIO]
    • Atmospheric Backdrop (Slate-950 + Multi-layer Radial Spotlights + 3D Grid)
    • Glassmorphic Containers (Frosted glass, specular top edge, spring entry)
    • Kinetic Typography (Staggered spring reveals, radiant gradient highlights)
    • Dynamic Telemetry (Interpolated count-up, Circular donut gauges, bar charts)
    • Architecture Conduits (Cubic bezier SVG wires + traveling comet pulses)
                                      │
                                      ▼
                       [AUDIO & BEAT-LOCKED TIMELINE]
    • Word-level speech alignment (Edge-TTS / Gemini Multimodal Persian TTS)
    • Beat-matched transitions (riser → impact → sparkle SFX)
                                      │
                                      ▼
                      [REMOTION 60FPS MASTER RENDER]
    • Sequence-local frame context preservation
    • Subframe motion blur & anti-jitter pixel rounding
    • MP4 Master + Contact Sheet Artifact
```

### Action Items for Implementation:
1. **Recipe Card System**: Add modular, reusable recipe templates to `src/motion/recipes/` based on the top 10 viral styles (SaaS Launch, Tech Architecture, Data Dashboard, Infinite Zoom, Kinetic Lyric).
2. **Showreel Persona Prompt Integration**: Add a dedicated prompt interpreter that recognizes viral triggers (`showreel`, `go all out`, `dribbble-level UI`) and automatically selects the highest-energy motion recipes.
3. **Sound FX Synchronization Layer**: Add audio transients (impact whooshes, digital clicks, riser sweeps) tied directly to frame impact points.
4. **Documentation & Skill Harmonization**: Keep `SKILL.md` updated with the dual-engine doctrine so users can request either technical scientific explainers or viral marketing motion graphics.
