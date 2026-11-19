---
layout: center
clicks: 2
---

<div class="kicker">Finding 1</div>

# Geospatial FMs lose about a third of their ID performance OOD

<div class="grid grid-cols-2 gap-16 mt-10">
  <BigNumber :value="32" suffix="%" label="average GFM drop with full fine-tuning" :step="$clicks" :at="1" />
  <BigNumber :value="34" suffix="%" label="average GFM drop with a frozen backbone" :step="$clicks" :at="2" />
</div>

<div v-click class="mt-10 muted">Comparable to the 14–30% gaps between ImageNet and ImageNet-V2.</div>

<!--
[30:00] Pause after the number lands. "Regardless of architecture, size, pretraining or fine-tuning strategy."
-->

---
clicks: 5
---

# It depends on the type of shift

<div class="grid grid-cols-5 gap-4 items-center">
<div class="col-span-3"><ShiftFits :step="$clicks" :show-tau="false" /></div>
<div class="col-span-2">

<div v-click="1"><b class="text-[#56B4E9]">Temporal:</b> almost on the diagonal, ~3% drop</div>
<div v-click="2" class="mt-3"><b class="text-[#0072B2]">Scale:</b> a third to a half lost</div>
<div v-click="3" class="mt-3"><b class="text-[#009E73]">Geographic:</b> the bigger the move, the bigger the drop</div>
<div v-click="4" class="mt-3"><b class="text-[#CC79A7]">Processing:</b> L2A → L1C hurts, varies by model</div>
<div v-click="5" class="mt-3"><b class="text-[#D55E00]">Sensor:</b> about half of ID performance lost</div>

</div>
</div>

<div class="cite">Linear fits OOD = m·ID + b per shift, frozen backbone (Fig. 2).</div>

<!--
[31:00–33:00] Each line is the best fit through every model–task point for that shift. Red dashed = no degradation.
-->

---
clicks: 3
---

# Robustness varies across shift type

<Spotlight src="/figures/paper/fig2_id_vs_ood_frozen.png" width="72%" :step="$clicks" :spots="[
  { x: 6.5, y: 3.5, w: 28, h: 41, at: 1, label: 'Temporal: points hug the diagonal' },
  { x: 71.5, y: 3.5, w: 27.5, h: 41, at: 2, label: 'Sensor: large, heterogeneous drops' },
  { x: 12.5, y: 76, w: 9.5, h: 10, at: 3, label: 'Germany → Cambodia, far below Denmark' },
]" />

<!--
Spot coordinates are % of the image; tweak in this file if a box is off.
-->

---
clicks: 1
---

# A bigger move means a bigger drop

<div class="grid grid-cols-2 gap-10 items-center mt-4">
<div class="flex justify-center">
  <IdOodSwap id="ftw_germany_image_id" ood="ftw_cambodia_image_ood" id-caption="FTW Germany (ID)" ood-caption="FTW Cambodia (OOD)" :step="$clicks" :at="1" :size="240" />
</div>
<div class="text-lg">

Fine-tuned on Germany, **every** model does substantially worse on Cambodia than on Denmark.

<div class="mt-4 muted">Different continent, field sizes, shapes and dominant crops vs. a neighbour with similar crops.</div>

</div>
</div>

---
clicks: 3
---

<div class="kicker">Finding 2</div>

# Pretraining on Earth Observation data does not mean models are robust to EO tasks

<Spotlight src="/figures/paper/fig3_ood_vs_er.png" width="92%" :step="$clicks" :spots="[
  { x: 4.5, y: 5, w: 46.5, h: 79, at: 1, label: 'Full fine-tuning' },
  { x: 84, y: 7, w: 14.5, h: 13, at: 2, label: 'CLIP and ImageNet ViT sit alongside the best GFM' },
  { x: 66.5, y: 71.5, w: 8, h: 9, at: 3, label: 'Some GFMs fall below the average model' },
]" />

<!--
GFMs show little to no robustness advantage over ImageNet / CLIP models (§6.2).
The next slide animates the same chart from data/model_summary.csv.
-->

---
clicks: 3
---

# Overall OOD vs effective robustness (animated)

<div class="grid grid-cols-2 gap-4 mt-1">
  <RobustnessMap protocol="FULL" title="Full fine-tuning" :step="$clicks" :legend="false" :width="430" />
  <RobustnessMap protocol="HEAD" title="Frozen backbone" :step="$clicks" :legend="false" :width="430" />
</div>
<div class="flex justify-center gap-8 text-sm mt-1">
  <span v-click="1"><span class="fam" style="background: var(--gfm)" />Geospatial FM</span>
  <span v-click="2"><span class="fam" style="background: var(--vfm)" />Generic pretrained</span>
  <span v-click="3"><span class="fam" style="background: var(--rnd)" />Random init</span>
</div>

<style>
.fam { display: inline-block; width: 11px; height: 11px; border-radius: 50%; margin-right: 6px; vertical-align: -1px; }
</style>

<!--
Click 1: GFMs. Click 2: generic pretrained. Click 3: random init.
Data: data/model_summary.csv, generated 17 Nov 2026 with
  npm run data -- ../CVPR/AllTasks_for_plotting-CVPR-Full.csv:FULL ../CVPR/AllTasks_for_plotting-CVPR-Head.csv:HEAD --id-col "Avg Test ID Acc" --ood-col "Avg Test OOD Acc" --points
HEAD (frozen) matches paper Fig. 3. FULL is close but not identical: the Full CSV has no RESISC45→UCMerced results for
clay, clip, croma, dinov3_large_sat and resnet50_imgnet. Re-run the command when those finish.
-->

---
clicks: 5
---

<div class="kicker">Finding 3</div>

# The best ID model isn't always the best OOD model

<KendallTau :step="$clicks" />

<div v-click="5" class="mt-6 text-center takeaway inline-block">Under sensor shift, ID rankings don't predict OOD rankings at all.</div>

<div class="cite">Kendall τ between models' ID and OOD scores, within task, averaged per shift (frozen backbone).</div>

---
clicks: 3
---

# One shift up close: <span style="color: #D55E00">Sensor shift</span>

<div class="flex justify-center">
<SlopeChart shift="Sensor" protocol="HEAD" :step="$clicks" :highlight="['clip', 'dofa']" />
</div>

<!--
Sensor shift, frozen backbone (data/model_summary.csv). Click 1: ID scores. Click 2: lines drop to OOD.
Click 3: highlight DOFA (a GFM) and CLIP (generic pretrained): they start and end in nearly the same place,
so EO pretraining buys no extra robustness here.
-->
