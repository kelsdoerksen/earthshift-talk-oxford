---
layout: center
clicks: 2
---

<div class="grid gap-4 items-center" style="grid-template-columns: 320px 1fr">
<div>

# Trained here.<br><span class="ood">Deployed there.</span>

<p v-click="1">A building-damage model trained on the <span class="id">Kahramanmaraş earthquake</span> (Türkiye–Syria) is used after the <span class="ood">Al Haouz earthquake</span> (Morocco).</p>

<p v-click="2" class="takeaway">Real deployments are almost always out-of-distribution.</p>

</div>
<div class="flex justify-center">
  <QuakeGlobe :step="$clicks" :arc-at="1" :width="540" :height="410" />
</div>
</div>

<div class="cite">Locations of the two BRIGHT earthquake events used in EarthShift's geographic shift (ID: Kahramanmaraş; OOD: Al Haouz). Insets: BRIGHT pre-event RGB samples.</div>

<!--
[0:30–2:00] The hook. Click 1: the arc flies from Kahramanmaraş (ID, the training events) to Al Haouz (OOD).
From the paper: "We use the samples from the Kahramanmaraş (Turkey–Syria) earthquake events as ID and samples from
the Al Haouz earthquake in Morocco as OOD."
Line to land: the model never gets to choose where it is used.
-->
