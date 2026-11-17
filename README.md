# EarthShift talk (Slidev)

A 45-minute talk deck: career path → state of geospatial AI → EarthShift results → takeaways.
Built with [Slidev](https://sli.dev) so slides, charts and animations are all code that Claude Code can edit.

## Quick start

```bash
npm install           # needs Node 18+
npm run dev           # opens http://localhost:3030 (presenter view: /presenter)
```

Then open this folder in Claude Code (`claude`). It reads `CLAUDE.md` for the house rules
(palette, "numbers only from data/", component list).

Optional: install the community Slidev skill so Claude knows Slidev's syntax well
(see https://www.skills.sh/antfu/skills/slidev), or point it at https://sli.dev/llms-full.txt.

## What's already here

- **Talk skeleton**: ~30 slides across `pages/01–06`, with presenter notes and target timestamps (`notes/talk-plan.md`).
- **Real assets from the paper**: 30 ID/OOD/label tiles cropped from Fig. 1 (`public/tiles/`), Figs. 1–3 (`public/figures/paper/`), Table 1 (`data/datasets.csv`), and every headline number with its page reference (`data/paper_numbers.json`).
- **Animated components** (`components/`): ID→OOD tile swaps, a five-shift gallery, an effective-robustness explainer, per-shift fit lines, Kendall τ bars, count-up stats, figure spotlights, a career timeline, and data-driven versions of Fig. 3 and an ID→OOD slope chart.
- **Results exporter** (`scripts/export_results.py`): turns per-task results into `data/model_summary.csv` using the paper's effective-robustness method (per-shift fit, ER centred per task, shifts weighted equally).

## Hooking up your results

1. Edit `data/task_to_shift.csv` so the `task` column matches the task names in your aggregation files.
2. Export one CSV per protocol with columns `Task, Model, Avg Test ID, Avg Test OOD` (column names can be changed with flags; see `--help`).
3. `npm run data -- results_full.csv:FULL results_head.csv:HEAD --points`
4. The `RobustnessMap` and `SlopeChart` slides switch from their empty-state card to the live chart. Check them against Fig. 3.

## Fill in

`grep -rn TODO pages data` lists everything only you can supply: career dates and roles, lessons, open questions, venue, links.

## Export

```bash
npm run export         # PDF (needs playwright-chromium, installed as a dev dependency)
npm run export:pptx    # PowerPoint with slide images, if a venue requires it
npm run build          # static site in dist/ (can be hosted on GitHub Pages)
```

Use `npx slidev export --with-clicks` to get one PDF page per animation step.

## Good prompts for Claude Code

- "Add a slide after the GFM boom slide with an animated bar chart of GFMs released per year. Put the data in data/gfm_releases.csv and leave the counts as TODO for me to fill."
- "Make the Sensor slope chart slide show full vs frozen side by side."
- "Tighten Part 2 to 8 minutes: suggest which slides to merge."
- "Walk through every slide in order and flag any number that isn't sourced from data/."
