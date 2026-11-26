---
layout: default
---

<GlobeNetwork />

<div class="relative z-10">
<div class="kicker">Part 2</div>

# The state of geospatial AI
</div>

<!--
[10:00] Part 2. Arc: what a GFM is → how you use one → there are many, all claiming SOTA → no leaderboard →
how to choose → the design choices (and the "particle" question) → deployment is OOD → open questions.
If running long, skip the two "particle" slides (marked optional in their notes).
-->

---
clicks: 3
---

# What is a geospatial foundation model?

<div class="text-lg leading-snug">
A <b>pretrained model</b>, usually trained with <b>self-supervision</b> on <b>unlabeled</b> data, that extracts
<b>generic features</b> useful for a wide <b>variety of downstream tasks</b>.
</div>

<div class="grid gap-6 mt-4 items-center" style="grid-template-columns: 560px 1fr">
<GfmPipeline :phase="$clicks >= 1 ? 2 : 1" head="none" :width="560" />
<div class="text-base leading-snug space-y-4">
  <div v-click="1">The output is an <b>embedding</b>: a feature vector, learned <b>without any labels</b>.</div>
  <div v-click="2">It is <b>not</b> the answer to your task (crop type, yield, flood extent). It has to be <b>adapted</b>.</div>
  <div v-click="3">The payoff: <b>better generalisation</b> and <b>fewer labels</b> than training from scratch.</div>
</div>
</div>

<!--
[10:00–11:00] Adapted from my TreeSense talk.
Click 1: the embedding box. Click 2: an embedding is not an answer. Click 3: why people use them.
Plant the seed: "better generalisation" is the claim EarthShift puts to the test in Part 3.
-->

---
clicks: 3
---

# How do I use a foundation model?

<div class="grid gap-4 mt-2 items-start" style="grid-template-columns: 560px 1fr">
<div>
<GfmPipeline :phase="2" :head="['none', 'knn', 'linear', 'finetune'][Math.min($clicks, 3)]" :width="560" />
</div>
<EmbeddingMap :mode="['raw', 'knn', 'linear', 'finetune'][Math.min($clicks, 3)]" :width="300" />
</div>

<div class="grid grid-cols-3 gap-4 mt-3 text-sm">
  <div v-click="1" class="mode"><b>k-NN probe</b> · frozen<br><span class="muted">Label a new image by its nearest labelled neighbours. No training.</span></div>
  <div v-click="2" class="mode"><b>Linear probe / light head</b> · frozen<br><span class="muted">Only the last layer learns: borders drawn over a fixed map.</span></div>
  <div v-click="3" class="mode ft"><b>Full fine-tuning</b><br><span class="muted">Every layer learns: the map itself moves.</span></div>
</div>

<style>
.mode { border-top: 4px solid #8fa3b8; padding-top: 6px; }
.mode.ft { border-top-color: var(--accent); }
</style>

<!--
[11:00–12:30] TreeSense slides 5–6 (frozen vs fine-tuned) merged with the "Evaluating a model on a dataset" idea from Hannah's SatSummit deck.
The right panel is a SKETCH (synthetic points), not data.
Click 1 k-NN: the circle reaches the new image's 5 nearest labelled examples in the frozen embedding.
In this sketch 3 of the 5 are peas, so k-NN calls a maize field "peas": the frozen embedding mixes them up.
Click 2 linear: regions drawn over the SAME dots; dashed rings = examples on the wrong side of a border.
Click 3 fine-tune: the backbone changes, so the dots move into tighter groups and the mistakes go away.
Say it: EarthShift tests both regimes (frozen backbone + light head, and full fine-tuning).
-->

---
clicks: 1
---

# An example dataset: EuroSAT

<EuroSatIntro :step="$clicks" />

<div class="cite">EuroSAT (Helber et al., 2019), MIT licence · modified Copernicus Sentinel-2 data. Adapted from H. Kerner, "State of GeoAI", SatSummit 2026 (Taylor Geospatial).</div>

<!--
Adapted from slide 10 of Hannah's SatSummit 2026 deck. Click 1: the image is one of EuroSAT's Sentinel-2 tiles (a river);
EuroSAT comes as 13 Sentinel-2 bands, RGB is only 3 of them. (m-EuroSAT is GEO-Bench's version of this dataset.)
-->

---
clicks: 11
---

# Embeddings in action: EuroSAT

<EuroSatProbe :step="$clicks" />

<div class="cite">EuroSAT (Helber 2019), MIT · Copernicus · DINOv2 small (frozen) · map: t-SNE detail, borders sketched in 2D · fine-tune: illustration (mock). Adapted from H. Kerner, "State of GeoAI", SatSummit 2026.</div>

<!--
Slide 11 (beats 1-12) of Hannah's SatSummit deck, rebuilt from its data (data/eurosat_probe.json).
0 A training image with a known label (River). 1 It goes into a frozen model. 2 Out come 384 numbers: its embedding.
3 Those numbers become one dot on a 2-D map. 4 Two more known images (Highway, Pasture) do the same.
5 100 EuroSAT training images. 6 Same-class images land near each other. 7 A new image, label unknown.
8 It lands among them ("Our image"). 9 k-NN: its 5 nearest vote, River 3 / 5. 10 Linear probe: borders drawn
over the same map, River. 11 Fine-tune: the model itself changes, so the dots move into tighter groups (illustration:
no fine-tune was run for this example).
-->

---
clicks: 3
---

# So many geospatial foundation models, all claiming state-of-the-art

<SotaWall :step="$clicks" :cards-at="1" :ask-at="2" :count-at="3" />

<div class="cite">Paper abstracts on arXiv, quoted verbatim (… = cut). A selection of models, not a rate. Via H. Kerner, SatSummit 2026.</div>

<!--
[12:30–13:30] Click 1: the cards land, each "state-of-the-art" gets highlighted. Click 2: which one is best? Click 3: and there are 75+.
GFMs look like the state of the art, but it's hard to know which is best, and many people don't know what all the options are.
Note: Galileo appears here as a field example; it is not one of the 12 models EarthShift evaluates.
-->

---
clicks: 2
---

# <span v-if="$clicks < 2">We have AI coding leaderboards</span><span v-else>But not for geospatial AI</span>

<Leaderboard :step="$clicks" :grow-at="1" :drain-at="2" />

<div class="cite" v-if="$clicks < 2">Artificial Analysis Coding Agent Index, as of 9 Nov 2026 (scores as displayed).</div>

<!--
[13:30–14:15] After Hannah's SatSummit deck, slides 3–4.
Click 1: a leaderboard everyone in LLMs looks at. Click 2: it drains; for GeoAI the form exists, nobody knows what goes in it.
-->

---

# How we measure progress today

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<v-clicks>

- **GEO-Bench** (2023) and **GEO-Bench-2** (2026): many tasks, one test set each
- Papers pick their own datasets, splits and settings, so reported numbers rarely line up
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
[14:15–15:30] Not a criticism of these benchmarks: they're what we need for method development. They answer a different question.
Bullet 2 is the point of Hannah's audit (same model, same dataset, different papers, different numbers).
-->

---
clicks: 4
---

# Choosing a model: things to consider

<div class="grid gap-8 mt-4 items-center" style="grid-template-columns: 330px 1fr">
<div class="text-lg space-y-3">
  <div v-click="1"><b>→ Ease of use</b><br><span class="muted text-base">weights, code, docs, input format</span></div>
  <div v-click="2"><b>→ Cost of use</b><br><span class="muted text-base">fine-tuning, inference, storage</span></div>
  <div v-click="3"><b>→ Your application</b><br><span class="muted text-base">your sensor and data, time series or not, task type</span></div>
  <div v-click="4"><b>→ Data coverage</b><br><span class="muted text-base">global, regional, species-specific?</span></div>
</div>
<figure class="m-0">
  <div class="text-sm font-bold" style="color: var(--accent)">AI × sustainability lens: compute cost</div>
  <img :src="$asset('/figures/external/olmoearth_fig1_macs.png')" class="w-full mt-1" alt="OlmoEarth Fig. 1: average score vs multiply-accumulate operations per example">
  <figcaption class="text-xs muted mt-1">OlmoEarth paper, Fig. 1: average score vs multiply-accumulate operations to encode one example (log x axis).</figcaption>
</figure>
</div>

<!--
[15:30–16:30] TreeSense slide 7. The bigger model isn't always the better one: the x axis spans four orders of magnitude.
Note: OlmoEarth and Galileo are in this figure but are NOT among the 12 models EarthShift evaluates (the paper excludes them).
Bridge: "your application" and "data coverage" are exactly where distribution shift comes in.
-->

---
clicks: 6
---

# Design choices behind every GFM

<DesignChoices :step="$clicks" :tag-at="6" />

<div v-click="6" class="mt-4 text-center text-lg">Every design choice is also a way the data can <span class="ood">shift</span> at deployment.</div>

<!--
[16:30–17:30] TreeSense slide 8, drawn with EarthShift tiles. One choice per click:
modality (S2 vs S1), time (France RPG 2017 → 2022), input shape (chip and patch grid), preprocessing (L1C → L2A), geography (Germany vs Cambodia).
Click 6: each gets the EarthShift shift type it sets up. This is the foreshadow for Part 3.
-->

---
clicks: 5
---

# Patches were designed for photos

<div class="ptable mt-4">
  <div class="ph"></div><div class="ph">Natural images (ImageNet)</div><div class="ph">Earth observation rasters</div>
  <template v-for="(r, i) in [
    ['Pixel size', 'no physical unit', '0.3 m to 1 km GSD: one 16×16 patch spans ~5 m to 16 km'],
    ['Channels', '3 (RGB)', '2 to 200+, different for every sensor'],
    ['Time', 'single frame', 'irregular series; clouds create missing pixels'],
    ['Objects', 'framed and centred by a photographer', 'fields, roads, animals ignore the grid; mixed pixels at boundaries'],
    ['Typical task', 'one label per image', 'often per-pixel (segmentation, crop-type maps)'],
  ]" :key="r[0]">
    <div v-click="i + 1" class="pk">{{ r[0] }}</div>
    <div v-click="i + 1" class="muted">{{ r[1] }}</div>
    <div v-click="i + 1">{{ r[2] }}</div>
  </template>
</div>

<div class="mt-5 text-lg">If the particle came from ImageNet conventions, are we inheriting assumptions that don't hold for us?</div>

<style>
.ptable { display: grid; grid-template-columns: 130px 1fr 1.6fr; gap: 9px 18px; font-size: 16px; }
.ptable .ph { font-weight: 700; font-size: 13px; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; border-bottom: 2px solid var(--rule); padding-bottom: 4px; }
.ptable .pk { font-weight: 700; }
</style>

<!--
[17:30–18:15] OPTIONAL (cut if running long). From my lab-meeting deck "Are pixels and patches the right particles for our data?".
A "particle" = the smallest unit a model sees; the thing that becomes one token.
-->

---
clicks: 6
---

# What is the particle?

<div class="muted">The smallest unit the model sees, the thing that becomes one token. Every architecture makes this choice, usually implicitly.</div>

<ParticleSpectrum :step="$clicks" />

<div v-click="6" class="mt-6 grid grid-cols-3 gap-4 text-sm">
  <div><b>1 · What is the particle?</b><br><span class="muted">fixed or learned from content?</span></div>
  <div><b>2 · How are particles ordered?</b><br><span class="muted">raster scan is a default, not a law</span></div>
  <div><b>3 · Compress first, or stay native?</b><br><span class="muted">what does the encoder throw away?</span></div>
</div>

<!--
[18:15–19:00] OPTIONAL. Purple = one particle. Same scene, five answers to "what is a token?"
Click 6: the three choices hiding inside "tokenize the image". Line to land on 3: small objects, rare classes,
and the cues that signal a distribution shift are prime suspects for what gets thrown away.
-->

---

# EO models already disagree on the particle

<div class="grid grid-cols-3 gap-4 mt-5">
  <div v-for="(m, i) in [
    ['Presto', 'a single pixel\'s time series', 'lightweight; per-pixel tokens across time and modalities'],
    ['Galileo', 'space × time × channel-group tokens', 'mixes global and local objectives over many modalities'],
    ['AnySat', 'patches defined in metres', 'one model across resolutions, scales and sensors'],
    ['Atomizer', 'one scalar: pixel × band', 'each token carries wavelength, bandwidth and GSD'],
    ['AlphaEarth', 'a 10 m embedding field', 'continuous-in-time embeddings; the map itself is the representation'],
    ['Our INR work', 'a coordinate query', 'the model is a function of (x, y, t); resolution-free by design'],
  ]" :key="m[0]" v-click class="pcard" :class="{ ours: i === 5 }">
    <div class="font-bold text-lg">{{ m[0] }}</div>
    <div class="text-sm mt-1" style="color: #7b3fa0"><b>Particle:</b> {{ m[1] }}</div>
    <div class="text-sm muted mt-2">{{ m[2] }}</div>
  </div>
</div>

<style>
.pcard { background: #f3f4f5; padding: 12px 16px; border-radius: 6px; min-height: 118px; }
.pcard.ours { background: #e6eeec; }
</style>

<!--
[19:00–19:30] OPTIONAL. Six cards, one per click. None of these are among EarthShift's 12 models; this is about the field.
-->

---
layout: default
---

<ApplicationsGlobe />

<div class="relative z-10 text-center mt-2">
<div class="kicker">The question</div>
<div class="text-3xl font-bold leading-snug mt-2 mx-auto" style="max-width: 820px">
Are geospatial foundation models robust to the distribution shifts encountered in real-world applications?
</div>
</div>

<!--
[19:30–20:00] One question. The applications around the globe are where GFMs are used: damage assessment (BRIGHT),
flood mapping (Sen1Floods11), crop mapping (France RPG), cloud segmentation (CloudSEN12), image classification (RESISC45).
Each one meets a different kind of shift once deployed. Bridge into Part 3.
-->
