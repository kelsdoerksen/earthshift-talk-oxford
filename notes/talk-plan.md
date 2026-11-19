# Talk plan: 45 min (≈40 min talk + 5 min Q&A)

| Time | Section | Slides (pages/) | Clicks |
|---|---|---|---|
| 0:00–2:00 | Cover + hook: trained here, deployed there | slides.md, 01-hook | 2 |
| 2:00–10:00 | **Part 1: How I got here** (career timeline, lessons, research threads) | 02-journey | 8 + 4 + 5 |
| 10:00–20:00 | **Part 2: State of geospatial AI** (what a GFM is, how to use one, all claiming SOTA, no leaderboard, ID benchmarks, choosing a model, design choices, particles, deployment is OOD, open questions) | 03-state-of-geoai | ~45 |
| 20:00–29:00 | **Part 3a: EarthShift setup** (question, 5 shifts, 18 tasks, models, effective robustness) | 04-earthshift-setup | 5 + 5 + 4 + 4 |
| 29:00–37:00 | **Part 3b: Results** (⅓ drop, by shift, geographic, GFM vs VFM, fine-tuning, rankings) | 05-earthshift-results | ~25 |
| 37:00–40:00 | **Part 4: Takeaways**, limitations | 06-takeaways | ~8 |
| +5 min | **Part 5: From benchmark to deployment** (npj landslide case study, operations checklist), thank you | 07-operations | ~22 |
| 40:00–45:00 | Q&A | | |

Slides to cut if running long: the three "particle" slides (Part 2: "Patches were designed for photos", "What is the particle?", "EO models already disagree"), "Research threads" (Part 1), "Robustness varies across shift type" (Fig. 2 spotlight), "One shift up close".

## Before the talk
- [ ] Fill every yellow TODO (`grep -rn TODO pages data`)
- [ ] Export results → `data/model_summary.csv`, then check RobustnessMap / SlopeChart against Fig. 3
- [ ] Decide whether to keep both the static Fig. 3 spotlight and the animated RobustnessMap
- [ ] Check the CVPR double-blind policy before presenting the submission or naming co-authors
- [ ] `npm run export` → PDF backup on a USB stick; test on the venue laptop or projector resolution
- [ ] Rehearse with presenter view (`/presenter`): notes include target timestamps
