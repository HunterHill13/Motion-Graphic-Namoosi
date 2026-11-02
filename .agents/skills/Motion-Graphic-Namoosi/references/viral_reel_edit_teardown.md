# Viral Reel Edit Teardown & Composition Anatomy

> Reverse-engineered from frame-by-frame analysis of 16 high-performing tech/explainer videos (2.5M+ views) from `kelano86/tool-reel-system`.

---

## 1. Measured Editorial Metrics

| Metric | Target Specification |
| :--- | :--- |
| **Video Dimensions** | 1080x1920 (Vertical 9:16) or 1920x1080 (Horizontal 16:9) |
| **Framerate** | 30.0 fps (frame-accurate programmatic timing) |
| **Cuts per Reel** | 18–24 cuts across 40–50 seconds |
| **Mean Shot Duration** | **2.0 seconds** (range: 0.35s punch cuts to 3.2s complex setups) |
| **Text Cadence** | 1–3 words changing every $0.4\text{s} - 0.7\text{s}$ |
| **Ground Recolor Rate** | Background hue shifts every 4.0s–8.0s to match the active topic |

---

## 2. The 6-Shot Taxonomy

Rather than switching merely between a title slide and content, broadcast shorts utilize six distinct visual setups:

1. **The Chapter Ordinal Card (Attention Reset Beat):**
   - Duration: $1.0\text{s} - 1.5\text{s}$.
   - Palette: Warm beige ground (`#E1D7C8`), bold coral ordinal text (`#E7896D`), and crisp white card.
   - Purpose: Acts as a psychological palate cleanser between major sections or list items.
2. **Graphics-Only Subject (Light Ground):**
   - Clean off-white background (`#F9F9F9`) with soft shadow texture.
   - High-contrast technical UI, diagram, or data chart floating in 3D perspective.
3. **Graphics-Only Subject (Dark Ground):**
   - Deep charcoal or near-black (`#111111`) with neon laser conduits or glowing CAD calipers.
4. **Subject Hero with Reactive Callout:**
   - Primary visual actor centered in 3D space with dynamic coral outline boxes (`#E7896D`) highlighting key functional areas.
5. **Macro Typography Statement:**
   - 3–4 monumental kinetic words filling $80\%$ of the viewport with rapid directional wipe.
6. **The Horizon Anthem (Outro / Climax):**
   - Expansive camera pull-back revealing the full interconnected constellation of ideas.

---

## 3. The Tri-Font Typographic System

Never use a single generic font family for all screen elements. Divide typography deliberately into three roles:

| Tier | Typeface Style | Role & Application |
| :--- | :--- | :--- |
| **Tier 1: Monumental Sans** | Heavy/Bold Sans-Serif (Yekan Bakh Heavy / Inter 900) | Core spoken Persian concepts, massive titles (140–200px). |
| **Tier 2: Serif Italic** | Editorial Serif Italic (Bricolage Grotesque / Playfair Italic) | Emphasized keywords, chapter ordinals (`FIRST`, `SECOND`), and expressive adjectives. |
| **Tier 3: Monospace Caps** | Precision Technical Mono (Space Mono / JetBrains Mono) | Metadata tags, micro-labels, timestamps, telemetry numbers, and CAD caliper readings. |

---

## 4. UI Focus & Annotation Boxes

When demonstrating an interface, document, or diagram:
- Do not let the eye wander across a busy screen.
- Draw a crisp **coral focus bounding box** (`border: 2px solid #E7896D`) around the active feature.
- The box animates using `strokeDashoffset` from 0 to 100% in 6 frames, snapping viewer gaze immediately to the target metric.
