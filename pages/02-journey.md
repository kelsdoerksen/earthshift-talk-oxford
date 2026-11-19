---
layout: section
---

<div class="kicker">Part 1</div>

# How I got here

<!--
[2:00] Transition: "Before the benchmark, a bit about the path that made me care about this problem."
-->

---
clicks: 6
---

# From satellite operations to geospatial AI

<CareerTimeline :step="$clicks" />

<!--
[2:30–6:00] One click per stop (data/career.json). Keep each stop to ~20 s; the story is the thread, not the CV.
JPL (2019) → Planet Labs (the globe under it is a schematic constellation) → Oxford DPhil → ESA Φ-lab (Frascati, Giga)
→ UNICEF (Children's Climate Risk Index) → ASU · University of Cape Town (Climate Risk Lab).
-->

---
clicks: 4
---

# Research themes

<div class="grid gap-6 items-center mt-2" style="grid-template-columns: 1fr 230px">
<ResearchThemes :step="$clicks" />
<div class="flex justify-center"><MiniOrbitGlobe :size="230" :sats="8" /></div>
</div>

<!--
[8:00–10:00] One theme per click. The operations theme comes back at the end of the talk
(landslide impact forecasting in Nepal, npj Natural Hazards).
-->
