---
layout: center
clicks: 2
---

<div class="grid grid-cols-2 gap-12 items-center">
<div>

# Trained here.<br><span class="ood">Deployed there.</span>

<p v-click="1">A building-damage model trained on one earthquake meets the next one somewhere else.</p>

<p v-click="2" class="takeaway">Real deployments are almost always out-of-distribution.</p>

</div>
<div class="flex gap-4 justify-center">
  <IdOodSwap id="bright_turkey_rgb_id" ood="bright_morocco_rgb_ood" id-caption="Kahramanmaraş, Türkiye (ID)" ood-caption="Al Haouz, Morocco (OOD)" :step="$clicks" :at="1" :size="220" />
</div>
</div>

<!--
[0:30–2:00] The hook. Click 1 swaps Türkiye → Morocco (BRIGHT pre-event RGB).
Line to land: the model never gets to choose where it is used.
-->
