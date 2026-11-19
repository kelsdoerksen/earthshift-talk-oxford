<script setup lang="ts">
// EuroSAT, introduced as in slide 10 (beats 1-2) of H. Kerner's "State of GeoAI" deck (SatSummit 2026):
// step 0: one EuroSAT image (Sentinel-2, a river) · step >= 1: the 13-band stack beside it ("RGB is 3 of them").
// Data: data/eurosat_probe.json (bands, classes); image: public/eurosat.
import D from '../data/eurosat_probe.json'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 99 })
const NB = 10, LS = 92, OX = 7, OY = 5
const layers = Array.from({ length: NB }, (_, k) => NB - k)
</script>

<template>
  <div class="es-intro">
    <div class="left">
      <div class="bands" :class="{ on: step >= 1 }">
        <svg :width="LS + NB * OX + 4" :height="LS + NB * OY + 4" class="stack">
          <rect v-for="b in layers" :key="b" :x="b * OX" :y="(NB - b) * OY" :width="LS" :height="LS" rx="2" fill="#f6f4ee" stroke="#3b1e1c" stroke-width="1.5" />
          <image :href="`/eurosat/${D.hero.id}.jpg`" x="0" :y="NB * OY" :width="LS" :height="LS" style="image-rendering: pixelated" />
          <rect x="0" :y="NB * OY" :width="LS" :height="LS" rx="2" fill="none" stroke="#3b1e1c" stroke-width="2" />
        </svg>
        <div class="txt">
          <div class="t1">{{ D.bands.total }} Sentinel-2 bands</div>
          <div class="t2">RGB is {{ D.bands.rgb }} of them</div>
          <div class="t3">+{{ D.bands.total - D.bands.rgb }} optional: {{ D.bands.optional }}</div>
        </div>
      </div>
      <div class="classes" :class="{ on: step >= 1 }">
        <div class="kicker">{{ D.classes.length }} land-cover classes</div>
        <span v-for="c in D.classes" :key="c" class="chip">{{ c }}</span>
      </div>
    </div>
    <img :src="`/eurosat/${D.hero.id}.jpg`" class="big" alt="A EuroSAT image: a river, Sentinel-2">
  </div>
</template>

<style scoped>
.es-intro { display: grid; grid-template-columns: 1fr 400px; gap: 30px; align-items: start; margin-top: 6px; }
.big { width: 400px; height: 400px; image-rendering: pixelated; border-radius: 6px; display: block; }
.bands, .classes { opacity: 0; transform: translateY(8px); transition: opacity 500ms, transform 500ms; }
.bands.on, .classes.on { opacity: 1; transform: none; }
.classes { transition-delay: 250ms; }
.bands { display: flex; gap: 22px; align-items: center; margin-top: 8px; }
.stack { flex: none; overflow: visible; }
.t1 { font-size: 22px; font-weight: 700; }
.t2 { font-size: 18px; margin-top: 4px; }
.t3 { font-size: 15px; color: var(--muted); margin-top: 6px; line-height: 1.35; }
.classes { margin-top: 26px; }
.chip { display: inline-block; font-size: 13.5px; padding: 3px 10px; margin: 0 6px 6px 0; border-radius: 999px; background: #f1efe9; border: 1px solid #ddd6c8; }
</style>
