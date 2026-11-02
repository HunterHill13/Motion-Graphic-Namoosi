# Production Contract & Quality Standard (v40.1)

## 1. Purpose & Enforcement
This contract defines the immutable standards that any future production video must satisfy before release.
A production that violates any clause in this contract is disqualified and blocked from final export.

---

## 2. Directing & Narrative Structure
1. **One Primary Visual Job Per Beat:**
   Every spoken semantic beat corresponds to exactly ONE primary visual job (Hook, Define, Benchmark, Escalate, Climax, Resolve). Simultaneous competing hero elements are strictly prohibited.
2. **Causal Event Graph:**
   Every visual state change must have an explicit, observable physical cause:
   $$\text{STATE} \to \text{ANTICIPATION} \to \text{CAUSE} \to \text{ACTION} \to \text{CONSEQUENCE} \to \text{SETTLE}$$
   Elements must never materialize from an empty void without a mechanical, spatial, or optical cause.
3. **No Orphan Element Discipline:**
   Every visible entity must have a documented relationship (`CAUSE`, `CONSEQUENCE`, `TRANSFORMATION`, `BRIDGE`, `SHARED_IDENTITY`, `MATERIAL_REACTION`, `SPATIAL_RELATION`). An element whose narrative utility ends must either fuse into the substrate or exit via momentum.
4. **The Removal Test:**
   If any graphic element, border, telemetry counter, or decorative glyph can be removed without harming narrative comprehension, it MUST be removed.

---

## 3. Motion & Physics
1. **Authored Non-Linear Velocity:**
   Movement must be authored using multi-phase keyframes (`evaluateAuthoredKeyframeTrack`) or calibrated physics springs. Generic uniform easing across different masses is prohibited.
2. **Anticipation & Release:**
   Heavy masses must demonstrate a negative anticipation dip or pre-roll tension before rapid acceleration.
3. **Mass & Volume Conservation:**
   Any deformation (squash or stretch) must conserve two-dimensional volume:
   $$\text{scaleX} \cdot \text{scaleY} = 1.0 \pm 0.02$$
4. **Momentum Transfer:**
   When an object decelerates or strikes another, kinetic energy must transfer into connected rails, conduits, or secondary entities.
5. **Intentional Stillness:**
   Following an arrival and settle, elements must lock into complete stability for 1.0s to 2.5s to permit viewer reading. Ambient floating, random jiggling, and artificial sinusoidal breathing are banned.

---

## 4. Camera Choreography
1. **Motivated Camera Moves:**
   The camera moves only when motivated by narrative scale or spatial revealing.
   - Pushes in for intimacy, gravity, or focus.
   - Cranes or pulls back to broaden scope or reveal the complete assembly.
   - Tilts/orbits to establish three-dimensional depth.
2. **Zero Ambient Jitter:**
   Continuous camera breathing or Perlin noise shake during static holds is prohibited.
3. **Seismic Shock Reaction:**
   High-inertia impacts trigger a damped 3-frame vertical camera kick ($+8\text{px} \to -4\text{px} \to 0\text{px}$).

---

## 5. Visual World & Typography
1. **Single World Canvas:**
   Narratives must unfold within a persistent, continuous physical or architectural environment. The slide-per-sentence paradigm (fading to black between sentences) is prohibited.
2. **Material & Lighting Coherence:**
   All elements in a scene share a consistent light source, ambient occlusion, and material palette (e.g. titanium plates, brushed steel, cadmium rim illumination).
3. **Dual-Script Architecture:**
   - Visual typography (`displayText`) must never display phonetic Arabic/Persian diacritics (harakat/tashdid).
   - Diacritics are strictly reserved for the phonetic TTS input (`speechText`).
4. **Zero-Subpixel Jitter:**
   All text coordinates must use hardware-accelerated integer locks (`Math.round`), `translate3d(0,0,0)`, and `backface-visibility: hidden` to prevent font rasterization blur.

---

## 6. Audio Architecture
1. **Exclusive Voice Pipeline:**
   All narration must be synthesized via the official Google Gemini Multimodal Audio API (`gemini-2.5-flash-preview-tts` with voice `Puck`). Falling back to Edge-TTS or robotic neural voices is an immediate disqualification.
2. **Acoustic Mastering & Dynamic Ducking:**
   - Master voiceover normalized to EBU R128 (-16 LUFS).
   - Background score dynamically ducks by -14 dB during vocal phrases via sidechain compression.
3. **Frame-Accurate SFX:**
   Sound effects (impacts, servos, swooshes) must synchronize within $\pm 2$ frames of physical visual contact.

---

## 7. Quality Assurance (QA) & Verification
Before marking any production as complete, the following checks must pass:
1. `TYPE_SAFETY_GATE`: `npx tsc --noEmit` returns exit code 0.
2. `FREEZE_DETECTION_GATE`: Automated CV checks confirm zero unintentional frozen frames.
3. `CAUSAL_AUDIT_GATE`: 100% of transitions have confirmed ancestor causes.
4. `ELEMENT_BUDGET_GATE`: Active screen elements capped at $\le 7$ at all times.
5. `PIXEL_VERIFICATION_GATE`: Output MP4 frames manually verified on key arrival and climax frames.
