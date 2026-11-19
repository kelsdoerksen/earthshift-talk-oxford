---
layout: default
---

<ShiftingGlobe />

<div class="relative z-10">
<div class="kicker">Part 3</div>

# EarthShift

<div class="muted text-lg">A benchmark for robustness to real-world distribution shifts in Earth observation</div>
</div>

<!--
The animation loops on its own: the deployment (OOD) distribution slides away from the training (ID) one,
once for each of the five shift types. For "Geographic" an arc flies from Germany to Cambodia; for the others the
same place turns orange (same place, different data). Illustration only: the curves are not results.
-->

---
layout: center
---

# The research question

<div class="text-3xl mt-6 leading-snug">
When a model is good <span class="id">in-distribution</span>,<br>
<span v-click>is it still good <span class="ood">out-of-distribution</span>?</span>
</div>

<div v-click class="mt-10 muted">Measure it with real, paired datasets instead of synthetic corruptions.</div>

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
clicks: 2
---

# In-distribution vs out-of-distribution

<IdOodIntro :step="$clicks" />

<!--
Click 0: train a field-boundary model on Germany. Click 1: test it on more of Germany: that's in-distribution (ID).
Click 2: test it on Cambodia: out-of-distribution (OOD). Benchmarks usually report the first; deployment looks like the second.
-->

---
clicks: 5
---

# Five kinds of real-world shift

<ShiftPairs :step="$clicks" />

<!--
[21:00–23:00] One shift per click; static ID (top) → OOD (bottom) pairs.
Scale: coarse → fine (and back). Temporal: same place, other year. Geographic: other country.
Sensor: optical → SAR (disaster response: S1 sees through clouds). Processing: L2A → L1C (no time for atmospheric correction).
-->

---
clicks: 5
---

# 18 tasks with paired ID / OOD test sets

<div class="mt-2" style="max-height: 420px; overflow: hidden;">
<DatasetTable :step="$clicks" />
</div>

<div class="cite">Table 1. ↔ = evaluated in both directions (two test cases).</div>

---

# Models and protocol

<div class="grid grid-cols-3 gap-6 mt-6">

<div v-click class="p-4 rounded" style="border-top: 5px solid var(--gfm)">

### 7 geospatial FMs
DOFA · CROMA · Clay · Prithvi-EO-2.0 · TerraFM · DINOv3 (SAT-493M) · TerraMind

</div>

<div v-click class="p-4 rounded" style="border-top: 5px solid var(--vfm)">

### 3 generic vision FMs
ResNet50 (ImageNet) · ViT-B/16 (ImageNet) · CLIP

</div>

<div v-click class="p-4 rounded" style="border-top: 5px solid var(--rnd)">

### 2 random-init baselines
ResNet50 · ViT-B/16

</div>

</div>

<div v-click class="mt-8 grid grid-cols-2 gap-6 text-lg">
<div><b>Two transfer protocols:</b> full fine-tuning · frozen backbone + light head</div>
<div><b>Scale:</b> 5 seeds per model–task, learning-rate sweeps, <b>20,000+ experiments</b></div>
</div>

---
clicks: 4
---

# How to compare robustness fairly

<div class="grid grid-cols-5 gap-4 items-center">
<div class="col-span-3"><EffectiveRobustness :step="$clicks" /></div>
<div class="col-span-2 text-base">

<div v-click="2">A raw <b>OOD − ID</b> gap rewards models that are bad everywhere.</div>

<div v-click="3" class="mt-4">Fit a baseline <b>β</b> over all models in a shift: the OOD score you'd <i>expect</i> for a given ID score.</div>

<div v-click="4" class="mt-4"><b>Effective robustness</b> ρ(f) = OOD(f) − β(ID(f)).<br>Above the line = more robust than expected.</div>

<div v-click="4" class="mt-4 small muted">We report ID, OOD and ρ together (Taori et al., 2020).</div>

</div>
</div>

<!--
[27:00–29:00] Models a, b, c are the worked example from §4.3. The β line here is illustrative (OOD = 0.8·ID); in the paper β is fit per shift type.
-->
