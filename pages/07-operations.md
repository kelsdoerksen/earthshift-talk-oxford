---
layout: default
---

<MiniOrbitGlobe :size="300" :sats="8" class="ops-globe" />

<div class="relative z-10">
<div class="kicker">Part 5</div>

# From benchmark to deployment

<div class="muted text-lg mt-2" style="max-width: 560px">Operationalising AI in the real world: a case study in forecasting landslide impacts in Nepal</div>
</div>

<style>
.ops-globe { position: absolute; right: 70px; top: 150px; }
</style>

<!--
Part 5. EarthShift asks whether models survive a shift. This part asks what else it takes for a model to be used at all.
Source: Doerksen et al., npj Natural Hazards (2026).
-->

---
clicks: 3
---

<script setup>
import npj from '../data/npj_numbers.json'
</script>

# Case study: monsoon-triggered landslide impacts in Nepal

<div class="grid gap-6 mt-2 items-start" style="grid-template-columns: 1.15fr 1fr">
<figure class="m-0">
  <img src="/figures/npj/fig1_context.png" class="w-full" alt="Fig. 1: Nepal elevation, landslide impacts in 2023 and 2024, population, impacts per year and per month">
  <figcaption class="text-xs muted mt-1">Fig. 1: study region, recorded landslide impacts (2023, 2024), population, impacts by year and by month (Bipad Portal).</figcaption>
</figure>
<div class="text-base space-y-4">
  <div v-click="1"><b>{{ npj.context.impact_events }}</b> recorded landslide impact events, <b>{{ npj.context.dead_or_missing }}</b> people dead or missing, <b>{{ npj.context.homes_destroyed }}</b> homes destroyed <span class="muted text-sm">({{ npj.context.period }})</span></div>
  <div v-click="2">Planning today uses <b>seasonal outlooks</b> ({{ npj.context.seasonal_outlook_lead }} ahead, coarse) or <b>{{ npj.context.short_term_forecast }} forecasts</b>. Nothing in between.</div>
  <div v-click="3" class="takeaway">Humanitarian end-users asked for a <b>{{ npj.setup.forecast_window_days }}-day lead time</b> at <b>district level</b>, so that is what we built.</div>
</div>
</div>

<div class="cite">{{ npj.citation }}, doi:{{ npj.doi }}</div>

<!--
The need came first: Sijapati et al. documented the humanitarian requirement for 2-week, district-level forecasts.
Nepal: ~80% of annual rainfall arrives with the monsoon; most recorded impacts happen June–September.
-->

---
clicks: 5
---

<script setup>
import npj from '../data/npj_numbers.json'
</script>

# Designing for the decision, not the leaderboard

<div class="grid gap-6 mt-1 items-start" style="grid-template-columns: 1fr 330px">
<div class="text-base space-y-3">
  <div v-click="1"><b>→ The unit of the decision.</b> Forecast per <b>district</b> ({{ npj.setup.districts }}), the level where disaster planning happens, not an arbitrary grid.</div>
  <div v-click="2"><b>→ The time of the decision.</b> A rolling <b>{{ npj.setup.forecast_window_days }}-day</b> window: long enough to act, short enough to keep skill.</div>
  <div v-click="3"><b>→ The cost of errors.</b> Missing a landslide is worse than a false alarm, so false negatives are weighted <b>{{ npj.operations.false_negative_weight }}×</b> in the loss, and <b>users set the decision threshold</b>.</div>
  <div v-click="4"><b>→ Data anyone can use.</b> Only free, open EO and forecast products, so the tool is free to run and maintain.</div>
  <div v-click="5"><b>→ Explainable by default.</b> Satellite embeddings (LandslideNet) feed a Random Forest, which gives feature importances.</div>
</div>
<figure class="m-0">
  <img src="/figures/npj/fig2_method.png" class="w-full" style="max-height: 395px; object-fit: contain" alt="Fig. 2: data extraction, LandslideNet embeddings, feature combination, district-level prediction">
  <figcaption class="text-xs muted mt-1">Fig. 2: data cube → LandslideNet embeddings → decision-tree classifier → district map.</figcaption>
</figure>
</div>

<!--
Each of these was a stakeholder conversation, not a modelling choice: "better to prepare for something that does not happen
than to be under-prepared for a landslide impact that does occur."
-->

---
clicks: 1
---

<script setup>
import npj from '../data/npj_numbers.json'
</script>

# Does it work through the monsoon?

<img src="/figures/npj/fig5_f1_monsoon.png" class="w-full mt-2" alt="Fig. 5: daily F1 through the 2023 and 2024 monsoon seasons">

<div v-click="1" class="takeaway mt-4 text-lg">Trained on {{ npj.setup.train_years }}, tested on {{ npj.setup.test_years }}: F1 of {{ npj.results.monsoon_f1 }} from {{ npj.results.monsoon_months }}, when most impacts happen.</div>

<div class="cite">Fig. 5: daily F1 of the 14-day forecast (lines) and districts with recorded impacts (grey bars). {{ npj.citation }}.</div>

<!--
Blue: engineered features only; orange / green: + 10 / 32 satellite embeddings. Embeddings help most around monsoon onset,
which matters when the monsoon starts early (as in 2024).
-->

---
clicks: 4
---

# What it takes to run it

<div class="flex justify-center mt-1">
<Spotlight src="/figures/npj/fig8_operational_tool.png" width="74%" :step="$clicks" :spots="[
  { x: 0, y: 0, w: 66, h: 21, at: 1, label: 'Start from the user\'s question: a date, and a forecast back' },
  { x: 0.5, y: 22, w: 46, h: 26, at: 2, label: 'Every red dashed line is a person: accounts and authentication' },
  { x: 64, y: 0.5, w: 35.5, h: 47.5, at: 3, label: 'A forecast file uploaded by hand: who does this every day?' },
  { x: 38, y: 66, w: 36, h: 33.5, at: 4, label: 'Output at the level decisions are made: districts' },
]" />
</div>

<div class="cite">Fig. 8: proof-of-concept operational tool (Google Colab, Drive and Earth Engine, chosen because they are free). Red dashed = human interaction required.</div>

<!--
The model is one box out of five. Most of the work in operations is everything around it: data procurement, accounts, latency,
manual steps, and who keeps it running each season.
-->

---
clicks: 3
---

<script setup>
import npj from '../data/npj_numbers.json'
</script>

# Distribution shift shows up in operations too

<div class="grid grid-cols-3 gap-5 mt-4">
  <div v-click="1" class="opcard">
    <div class="kicker" style="color: var(--ood)">Input product shift</div>
    <div class="flex items-center gap-2 mt-3 mb-3">
      <span class="pill id-pill">trained on UKMO</span><span class="text-xl">→</span><span class="pill ood-pill">run on ECMWF</span>
    </div>
    UKMO forecasts had severe gaps in 2024; ECMWF is available fastest ({{ npj.operations.ecmwf_lag_days }} days). Fix: a monthly affine transform plus <b>adapting batch-norm statistics</b> to the new product.
  </div>
  <div v-click="2" class="opcard">
    <div class="kicker" style="color: var(--ood)">Label / reporting shift</div>
    <div class="text-3xl font-bold mt-2 mb-2" style="color: var(--ood)">+{{ npj.operations.impact_increase_2023_2024 }}</div>
    recorded impacts from 2023 to 2024. More landslides, or more reporting? The model can't tell, so <b>retrain every season</b>.
  </div>
  <div v-click="3" class="opcard">
    <div class="kicker" style="color: var(--id)">Robust by design</div>
    <div class="flex items-center gap-2 mt-3 mb-3"><span class="pill">KMA</span><span class="pill">UKMO</span><span class="pill">NCEP</span></div>
    Performance is consistent across forecast products, so an outage of any one product does not stop the forecast.
  </div>
</div>

<div v-click="3" class="takeaway mt-6 text-lg">The same lesson as EarthShift: measure performance under the shifts you will meet, and plan how to adapt.</div>

<style>
.opcard { background: #f6f7f8; border-radius: 8px; padding: 14px 16px; font-size: 14.5px; line-height: 1.4; min-height: 210px; }
.pill { display: inline-block; padding: 2px 10px; border-radius: 999px; background: #e5e7eb; font-weight: 700; font-size: 13px; }
.id-pill { background: var(--id); color: white; }
.ood-pill { background: var(--ood); color: white; }
</style>

<!--
Batch-norm adaptation to the deployment distribution is a simple form of test-time adaptation: the open direction from the EarthShift takeaways.
-->

---
clicks: 6
---

# Before you deploy AI in the real world

<div class="grid grid-cols-2 gap-x-10 gap-y-4 mt-4 text-base">
  <div v-click="1"><b>1 · Start from the decision.</b><br><span class="muted">Who acts, with what lead time, at what spatial unit?</span></div>
  <div v-click="2"><b>2 · Check the inputs exist at inference time.</b><br><span class="muted">Latency, cost, licences, outages, a backup product.</span></div>
  <div v-click="3"><b>3 · Expect shift.</b><br><span class="muted">New sensors, products, places, years. Test OOD before you deploy.</span></div>
  <div v-click="4"><b>4 · Choose your errors.</b><br><span class="muted">What does a miss cost vs a false alarm? Let users set the threshold.</span></div>
  <div v-click="5"><b>5 · Know what your labels measure.</b><br><span class="muted">Recorded impacts are not all landslides; reporting changes over time.</span></div>
  <div v-click="6"><b>6 · Plan for people and maintenance.</b><br><span class="muted">Manual steps, accounts, retraining each season, explanations users trust.</span></div>
</div>

<div v-click="6" class="takeaway mt-8 text-lg">An accurate model in-distribution is where deployment starts, not where it ends.</div>

<!--
Synthesised from the npj Natural Hazards paper (operational tool, stakeholder-driven design) and EarthShift (test OOD).
-->

---
layout: center
class: text-center
---

<OrbitBackground />

<div class="relative z-10 flex flex-col items-center">

# Thank you

<img src="/photos/headshot.jpg" class="headshot mt-4" alt="Dr. Kelsey Doerksen">

<div class="mt-4 text-xl font-bold">Dr. Kelsey Doerksen</div>
<div class="muted">ASU · University of Cape Town · Climate Risk Lab</div>
<div class="mt-3 text-lg"><a href="mailto:kdoerkse@asu.edu">kdoerkse@asu.edu</a></div>

</div>

<style>
.headshot { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; object-position: 50% 50%; border: 4px solid white; box-shadow: 0 2px 10px rgba(0,0,0,.18); }
</style>
