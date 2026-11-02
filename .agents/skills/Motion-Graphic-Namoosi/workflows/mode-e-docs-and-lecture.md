# WORKFLOW: MODE E — DOCUMENT / SLIDES / LECTURE TO VIDEO

## Overview
Triggered when the user provides slides (PPTX/PDF), documents (DOCX/PDF), textbook chapters, or recorded lectures.

```text
DOCUMENT / SLIDES / LECTURE
            ↓
INFORMATION EXTRACTION & TOPIC GRAPH
            ↓
FACTUAL GROUNDING & CITATION EXTRACTION (sources.md)
            ↓
EDUCATIONAL STORYTELLING & NARRATION SYNTHESIS
            ↓
SCHEMATIC DIAGRAM TRANSLATION
            ↓
TIMING & STORYBOARD
            ↓
PILOT GATE → BUILD → QC → DELIVERY
```

## Step-by-Step Instructions
1. **Extract Core Claims & Data**: Parse slides, tables, figures, formulas, and speaker transcripts.
2. **Build Source Traceability Ledger**: Populate `research/sources.md` with slide/page citations for every claim.
3. **Structure Educational Narrative**: Transform bullet points into a dynamic story arc (Hook -> Core Concept -> Mechanism -> Clinical/Practical Implication -> Summary).
4. **Convert Static Diagrams into Dynamic Schematics**: Use one-stroke vector diagrams (`schematic.tsx`) to illustrate pathways and mechanisms sequentially rather than presenting full static charts.
5. **Enforce Medical/Scientific QC**: Verify 0 hallucinated facts or mechanisms.
6. **Pilot & Production**: Standard pilot verification and build.
