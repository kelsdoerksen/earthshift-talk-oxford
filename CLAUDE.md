# EarthShift talk: instructions for Claude Code

A 45-minute Slidev talk: (1) Kelsey's path into geospatial AI, (2) the state of geospatial AI,
(3) EarthShift results, (4) takeaways. The source paper is the CVPR 2027 submission (keep a copy at
`refs/EarthShift_CVPR_MainText_Submission.pdf`; it is not committed).

## Commands
- `npm install`, then `npm run dev` (http://localhost:3030; presenter view at /presenter)
- `npm run export` → PDF backup · `npm run build` → static site in `dist/`
- `npm run data -- full.csv:FULL head.csv:HEAD` → regenerates `data/model_summary.csv`
- Slidev docs for LLMs: https://sli.dev/llms-full.txt (read this before using unfamiliar Slidev features)

## Layout
- `slides.md`: headmatter + cover; imports `pages/*.md` in order
- `pages/`: one file per talk section; presenter notes go in `<!-- -->` at the end of each slide
- `components/`: Vue components, auto-registered (use `<Name />` directly in markdown)
- `data/`: the only place numbers come from (see the rules below)
- `public/tiles/`: 30 ID/OOD/label tiles cropped from paper Fig. 1 (`clean/`: badge-free crops) · `public/figures/paper/`: Figs. 1–3 · `public/figures/external/`: third-party figures
- `utils/csv.ts`: CSV parser, scale helpers, shift and family colours

## Hard rules
1. **Never type a result number into a slide.** Numbers come from `data/paper_numbers.json`
   (copied from the paper, with page refs), `data/datasets.csv` (Table 1) or `data/model_summary.csv`
   (exported results). Field-level facts for Part 2 (not EarthShift results) live in `data/state_of_geoai.json`, and the npj landslide paper's numbers (Part 5) in `data/npj_numbers.json`, with sources. If a number isn't there, ask; don't estimate one from a figure.
2. Results phrasing must match the paper: "little to no robustness advantage", "similar or sometimes worse",
   "about a third". The pretraining-bias explanation is a *hypothesis*; keep the hedge.
3. The paper evaluates **12 models** (7 GFMs, 3 VFMs, 2 random init). Galileo and OlmoEarth are excluded.
4. Colours: ID `#0072B2` (`.id`, `var(--id)`), OOD `#D55E00` (`.ood`, `var(--ood)`).
   Model families: GFM blue, generic pretrained orange, random green (as in Fig. 3).
   Shift colours live in `SHIFT_COLORS` in `utils/csv.ts`; keep them consistent across slides.
5. Font: Liberation Sans / Helvetica / Arial (matches the paper figures). No web fonts: the deck must work offline.
6. Yellow `.todo` spans mark content only Kelsey can supply. Don't invent career details to fill them.

## Animation conventions
- Step-driven components take `:step="$clicks"`; the slide sets `clicks: N` in frontmatter.
  Components default to `step = 99` (fully revealed), so they also look right in exports and overview.
- Animate SVG lines with `stroke-dasharray` / `stroke-dashoffset` (SVG geometry attributes don't CSS-transition).
- Use `<Spotlight>` to walk through a static paper figure: spots are % boxes with an `at` click index.
- Keep each animation under ~1 s; one idea per click.

## Components
| Component | What it does | Data |
|---|---|---|
| `IdOodSwap` | Cross-fades an ID tile into its OOD tile (step or auto-loop) | `public/tiles` |
| `ShiftGallery` | Five shift types, one per click, each looping ID ↔ OOD (no longer used in the deck) | `public/tiles` |
| `ShiftPairs` | Five shift types as static ID → OOD pairs, one column per click | `public/tiles` |
| `IdOodIntro` | Train on Germany → test on Germany (ID) vs Cambodia (OOD), with definitions | `public/tiles` |
| `GlobeNetwork` | Part 2 opener: satellites image a dot-globe, images feed a network, apps light up (loops) | `globe_land.json` |
| `ShiftingGlobe` | Part 3 opener: globe + ID/OOD distributions sliding apart per shift type (loops) | `globe_land.json` |
| `QuakeGlobe` | Hook: Kahramanmaraş (ID) → Al Haouz (OOD) arc on a globe, with BRIGHT insets | `globe_land.json` |
| `ApplicationsGlobe` | Research-question slide: globe + five application tiles, highlight cycles | `public/tiles/clean` |
| `MiniOrbitGlobe` | Small globe with satellites (career timeline, Part 5 opener) | `globe_land.json` |
| `ResearchThemes` | Four research-theme cards with line icons | `npj_numbers.json` |
| `EuroSatIntro` | EuroSAT image, then 13-band stack and 10 classes (after H. Kerner's SatSummit slide 10) | `eurosat_probe.json`, `public/eurosat` |
| `EuroSatProbe` | 12-beat embeddings walkthrough: frozen DINOv2 → 384 numbers → t-SNE map → k-NN / linear / fine-tune (SatSummit slide 11) | `eurosat_probe.json` |
| `DatasetTable` | Table 1, one shift group per click | `data/datasets.csv` |
| `EffectiveRobustness` | 4-step explainer of ρ = OOD − β(ID) with the paper's a/b/c example | `paper_numbers.json` |
| `BigNumber` | Count-up headline stat | props |
| `ShiftFits` | Per-shift linear fits from Fig. 2 drawn one per click | `paper_numbers.json` |
| `KendallTau` | ID-vs-OOD rank agreement per shift, bars grow per click | `paper_numbers.json` |
| `RobustnessMap` | Animated Fig. 3 (OOD vs effective robustness, by family) | `model_summary.csv` |
| `SlopeChart` | ID → OOD per model for one shift, lines "fall" on click | `model_summary.csv` |
| `CareerTimeline` | Career stops, one per click | `data/career.json` |
| `Spotlight` | Dim-and-highlight regions of a static figure | image + spots |
| `OrbitBackground` | Animated satellite ground tracks for cover/end slides | none |
| `GfmPipeline` | Pretraining tiles → network → embedding, then a k-NN / linear / fine-tune head | `public/tiles/clean` |
| `EmbeddingMap` | 2-D embedding sketch: k-NN circle, linear regions, fine-tune tightening (synthetic) | none (seeded) |
| `SotaWall` | Verbatim "state-of-the-art" abstract excerpts, highlighted, then "Which one is best?" | `state_of_geoai.json` |
| `Leaderboard` | Coding-agent leaderboard grows, then drains to "?" rows | `state_of_geoai.json` |
| `DesignChoices` | GFM design choices, one per click, each tagged with the shift type it sets up | `public/tiles/clean` |
| `ParticleSpectrum` | Pixel / patch / adaptive / scalar / coordinate "particles", one per click | none |

## Checking work
After editing, run `npm run dev` and click through every changed slide, both forwards and backwards.
Before the talk, `npm run export` and open the PDF to check nothing overflows the slide.
