# The Look, Pacing, and Camera Grammar Manual

> Synthesized from empirical analysis of broadcast motion graphics, Pixar framing grammar, and procedural Remotion systems (`what-if-animation`).

---

## 1. Pacing & Cadence Laws

Programmatic animation often fails because cuts are paced by a metronome rather than narrative urgency. Follow these concrete numerical contracts:

| Metric | Fast-Paced Viral Profile | Documentary / Educational Profile |
| :--- | :--- | :--- |
| **Cuts per minute (Opening)** | **20 to 30 cuts/min** (approx. one cut every 2.0s–3.0s) | **8 to 15 cuts/min** (approx. one cut every 4.0s–7.5s) |
| **Median Shot Length** | **1.2s to 2.2s** (minimum 0.7s, maximum 2.8s) | **4.0s to 6.0s** |
| **Static Hold Ceiling** | **Strictly ZERO static hold > 3.0s** | Continuous subtle camera drift ($v \ne 0$) |
| **Word-Cut Synchronization** | Cuts land **2 frames prior** to the vocalized cue word | Cuts land on rhythmic downbeats (`snapToBeat`) |

### The Alternating Framing Law (Anti-Repetition)
Cuts must come from **changing shot size and angle**, never merely translating the camera inside the same framing:
1. **Establishing Wide:** The whole lit environment, primary actor small and grounded ($Z = 0$, camera FOV wide).
2. **Macro Insert:** An isolated physical object huge in frame with shallow focus (a chip, dial, document edge, caliper), often top-down ($45^\circ-90^\circ$ pitch).
3. **Medium Master:** Subject waist-up, camera zoom $1.6\times$ to $2.0\times$.
4. **Close-Up:** Focal actor head/face, camera zoom $3.0\times$ to $4.5\times$ for extreme punch.
5. **Over-The-Shoulder / Depth Layer:** Blurred foreground silhouette occupying $\ge 25\%$ of viewport width in plane $Z = +120$.
6. **High / Low Angle:** Looking down at a technical diagram ($+35^\circ$ tilt) or looking up from low ground ($-25^\circ$ tilt) toward the horizon.

> **RULE:** No two neighboring scenes may share the same shot size and camera pitch.

---

## 2. Motivated Practical Lighting Doctrine

Light does 80% of the cinematic work. Flat ambient lighting screams "AI prototype."

1. **Every Light Originates from an Identifiable Fixture:**
   - A visible ceiling pendant lamp, a warm desk lamp fixture, a sunlight angle from an off-screen window, or a luminous terminal slit.
2. **Dark Mid-Tones & Holes of Light:**
   - Walls and ambient canvas ground are kept in dark/mid-dark tones (`LightVeil`).
   - The primary subject sits inside or against a pool of light cast by the visible source.
3. **Directional Specular Rim Lighting:**
   - Primary actors must feature a warm edge highlight (`rimR` or `rimL`) along the silhouette boundary facing the fixture.
   - For dramatic pivots or paradigm shifts, swap to high-contrast cyan or coral rim (`rimAccent`).
4. **Volumetric Dust & Haze:**
   - Dynamic micro-particles drifting slowly across the illumination cone with Brownian motion (`VolumetricDustMotes`).
   - Depth-of-field blur: foreground dark elements blurred (`blur(12px)`), focal subject razor-sharp, background subtly softened (`blur(6px)`).

---

## 3. The Living Frame Invariant (Continuous Micro-Life)

A settled spring must never result in an absolute freeze ($v = 0$):
- **Breathing Camera Dolly:** Continuous micro-zoom ($1.00\times \rightarrow 1.03\times$) or micro-pan across the spoken phrase.
- **Secondary Atmospheric Drifting:** Floating dust motes, subtle light intensity pulse ($\pm 4\%$), oscillating laser conduit, or slowly incrementing metric counter.
- **Instant Expression & State Swaps:** Visual actors swap states cleanly on action beats or blinks rather than sluggish linear morphing.

---

## 4. Pre-Flight Visual Verification Checklists

### 4.1 Storyboard Sheet Inspection (`out/storyboard.jpg`)
1. **One-Second Phone Read:** Can a viewer understand the focal hierarchy at mobile resolution within 1.0 second?
2. **Framing Variety:** Does the sheet exhibit alternating shot sizes (Wide, Macro, Medium, Close-up, High/Low angle)?
3. **Visible Practical Light:** Does every shot show or imply an explicit directional light source?
4. **Subject Contrast:** Is the primary actor the highest-contrast, sharpest object in its depth plane?
5. **No Floating Entities:** Do standing elements have grounded contact shadows?

### 4.2 Motion Grid Flipbook Inspection (`out/motiongrid.png`)
1. **Physical Anticipation:** Is there a 2-frame crouch or wind-up before major velocity bursts?
2. **Momentum Handoff:** Does the camera absorb the impact shock on heavy landings?
3. **Spring Settle:** Does the element settle crisply without loose, floaty rubber oscillations?
4. **No Frame Pops:** Elements do not abruptly vanish or teleport between frames without motivated wipes or occlusion.
