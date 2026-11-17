---
layout: section
---

<div class="kicker">Part 2 · ~10 min</div>

# The state of geospatial AI

---

# The geospatial foundation model boom

<div class="grid grid-cols-4 gap-3 mt-6 text-center">
  <div v-for="(m, i) in ['DOFA','CROMA','Clay','Prithvi-EO-2.0','TerraFM','DINOv3-SAT','TerraMind','TODO: + others']" :key="m"
       v-click class="p-3 rounded border font-bold" :class="{ todo: m.startsWith('TODO') }">{{ m }}</div>
</div>

<div v-click class="mt-8 grid grid-cols-3 gap-6 text-sm">
  <div><b>Modalities</b><br>single-sensor optical · SAR–optical · many-modality</div>
  <div><b>Objectives</b><br>masked autoencoding · contrastive · self-distillation · generative</div>
  <div><b>Scale</b><br>native resolution 0.6–30 m · 87M–304M parameters</div>
</div>

<div class="cite">Ranges are for the seven GFMs evaluated in EarthShift.</div>

<!--
[10:00–12:00] TODO: add a "number of GFMs over time" chart if you have the data (a good place for a growth animation).
-->

---
layout: center
---

# The promise

<div class="text-2xl mt-6 leading-relaxed">

Pretrain one backbone on huge, diverse Earth observation archives <span v-click>→ reuse it cheaply</span> <span v-click>across <span class="id">sensors</span>, <span class="id">geographies</span>, <span class="id">label regimes</span> and <span class="id">tasks</span>.</span>

</div>

<div v-click class="mt-10 text-xl">So: <b>does it actually transfer?</b></div>

---

# How we measure progress today

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<v-clicks>

- **GEO-Bench** (2023) and **GEO-Bench-2** (2026): many tasks, one test set each
- Test samples closely resemble the training data → **in-distribution (ID)** scores
- Leaderboards rank models by ID score: nothing tells a practitioner which model survives a shift

</v-clicks>

</div>
<div v-click class="flex items-center">
<div class="text-2xl font-bold leading-snug">
"No one knows the state of the art in geospatial foundation models"
<div class="text-sm muted mt-2 font-normal">Corley et al., 2026 (paper title)</div>
</div>
</div>
</div>

<!--
[13:00–15:00] Not a criticism of these benchmarks: they're what we need for method development. They answer a different question.
-->

---
clicks: 2
---

# Deployment is out-of-distribution

<div class="grid grid-cols-3 gap-8 items-center mt-6">
  <BigNumber :value="30" suffix="%" label="drop in building-damage accuracy at a new disaster site" :step="$clicks" :at="1" />
<div v-click="2" class="col-span-2 text-lg">

- Field delineation models fail in new countries with different farming and climate patterns (Kerner et al., 2023)
- "Satellite data is a distinct modality in machine learning" (Rolf et al., ICML 2024)
- Most robustness work uses **synthetic** shifts (noise, clouds, blur), and robustness to those does not represent robustness to **natural** shifts (Taori et al., 2020)

</div>
</div>

<div class="cite">Building-damage figure: Benson &amp; Ecker, 2020, as cited in EarthShift §2.</div>

---

# Open questions in the field

<v-clicks>

- <span class="todo">TODO: your view</span> e.g. which pretraining data actually helps?
- <span class="todo">TODO</span> e.g. evaluation that matches how models are used
- <span class="todo">TODO</span> e.g. who gets good models: data coverage in the Global South
- **Do foundation models make us robust to the shifts we actually meet?** ← EarthShift

</v-clicks>

<!--
[18:00–20:00] Last bullet bridges into Part 3.
-->
