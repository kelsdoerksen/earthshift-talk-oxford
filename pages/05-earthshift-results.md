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

# Where the models actually sit

<Spotlight src="/figures/paper/fig2_id_vs_ood_frozen.png" width="72%" :step="$clicks" :spots="[
  { x: 6.5, y: 3.5, w: 28, h: 41, at: 1, label: 'Temporal: points hug the diagonal' },
  { x: 72, y: 3.5, w: 28, h: 41, at: 2, label: 'Sensor: large, heterogeneous drops' },
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

# Earth observation pretraining doesn't buy robustness

<Spotlight src="/figures/paper/fig3_ood_vs_er.png" width="92%" :step="$clicks" :spots="[
  { x: 4.5, y: 5, w: 46.5, h: 79, at: 1, label: 'Full fine-tuning' },
  { x: 84, y: 7, w: 14.5, h: 13, at: 2, label: 'CLIP and ImageNet ViT sit alongside the best GFM' },
  { x: 66.5, y: 71.5, w: 8, h: 9, at: 3, label: 'Some GFMs fall below the average model' },
]" />

<!--
GFMs show little to no robustness advantage over ImageNet / CLIP models (§6.2).
Swap this for <RobustnessMap :step="$clicks" protocol="HEAD" /> once data/model_summary.csv is filled.
-->

---
clicks: 3
---

# Overall OOD vs effective robustness (animated)

<div class="flex justify-center"><RobustnessMap protocol="FULL" :step="$clicks" /></div>

<!--
Click 1: GFMs. Click 2: generic pretrained. Click 3: random init.
Needs data/model_summary.csv (scripts/export_results.py). Shows an empty-state card until then.
-->

---

<div class="kicker">Finding 3</div>

# Fine-tuning the encoder doesn't fix it

<div class="grid grid-cols-2 gap-10 mt-8 text-lg">

<div v-click>

When the encoder is fine-tuned too, **robustness does not improve, and sometimes gets worse**.

</div>

<div v-click class="takeaway">

Better adaptation to the training distribution ≠ better generalisation beyond it.

</div>

</div>

<div v-click class="mt-10">
  <span class="todo">TODO: drop in a full vs frozen comparison, e.g. two &lt;SlopeChart&gt;s side by side for Scale</span>
</div>

---
clicks: 5
---

<div class="kicker">Finding 4</div>

# The best ID model isn't always the best OOD model

<KendallTau :step="$clicks" />

<div v-click="5" class="mt-6 text-center takeaway inline-block">Under sensor shift, ID rankings don't predict OOD rankings at all.</div>

<div class="cite">Kendall τ between models' ID and OOD scores, within task, averaged per shift (frozen backbone).</div>

---
clicks: 3
---

# One shift up close

<div class="flex justify-center">
<SlopeChart shift="Sensor" protocol="HEAD" :step="$clicks" :highlight="['clip', 'dofa']" />
</div>

<!--
Click 1: ID scores. Click 2: lines drop to OOD. Click 3: highlight models.
TODO: choose the shift and models to spotlight; needs data/model_summary.csv.
-->
