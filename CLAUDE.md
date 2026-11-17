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
- `public/tiles/`: 30 ID/OOD/label tiles cropped from paper Fig. 1 · `public/figures/paper/`: Figs. 1–3
- `utils/csv.ts`: CSV parser, scale helpers, shift and family colours

## Hard rules
1. **Never type a result number into a slide.** Numbers come from `data/paper_numbers.json`
   (copied from the paper, with page refs), `data/datasets.csv` (Table 1) or `data/model_summary.csv`
   (exported results). If a number isn't there, ask; don't estimate one from a figure.
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
| `ShiftGallery` | Five shift types, one per click, each looping ID ↔ OOD | `public/tiles` |
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

## Checking work
After editing, run `npm run dev` and click through every changed slide, both forwards and backwards.
Before the talk, `npm run export` and open the PDF to check nothing overflows the slide.
