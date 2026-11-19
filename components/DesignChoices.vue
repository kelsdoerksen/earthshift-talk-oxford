<script setup lang="ts">
// GFM design choices (after Kelsey's TreeSense talk, slide 8), one per click, each drawn with EarthShift tiles.
// At step >= tagAt every choice gets the EarthShift shift type it sets up (SHIFT_COLORS), to foreshadow Part 3.
import { SHIFT_COLORS } from '../utils/csv'

const props = withDefaults(defineProps<{ step?: number; tagAt?: number; size?: number }>(),
  { step: 99, tagAt: 6, size: 92 })

const choices = [
  { q: 'Which modality?', shift: 'Sensor', kind: 'stack', a: 'sen1floods11_s2_id', b: 'sen1floods11_s1_ood', note: 'optical · SAR · multispectral' },
  { q: 'How to treat time?', shift: 'Temporal', kind: 'time', a: 'rpg_2017_id', b: 'rpg_2022_ood', note: 'single date or time series' },
  { q: 'What input shape?', shift: 'Scale', kind: 'grid', a: 'chesapeake_naip_ood', b: '', note: 'chip size · patch size · resolution' },
  { q: 'What preprocessing?', shift: 'Processing', kind: 'proc', a: 'cloudsen12_l1c_ood', b: 'cloudsen12_l2a_id', note: 'processing level, normalisation' },
  { q: 'Where on Earth?', shift: 'Geographic', kind: 'pair', a: 'ftw_germany_image_id', b: 'ftw_cambodia_image_ood', note: 'what the pretraining data covers' },
]
const src = (n: string) => `/tiles/clean/${n}.png`  // badge-free crops of the EarthShift tiles
</script>

<template>
  <div class="row">
    <div v-for="(c, i) in choices" :key="c.q" class="col" :class="{ on: step >= i + 1 }">
      <div class="vis" :style="{ height: `${size + 26}px` }">
        <template v-if="c.kind === 'stack'">
          <img :src="src(c.b)" class="t" :style="{ width: `${size}px`, left: '30px', top: '0px' }">
          <img :src="src(c.a)" class="t" :style="{ width: `${size}px`, left: '8px', top: '20px' }">
        </template>
        <template v-else-if="c.kind === 'time' || c.kind === 'pair'">
          <img :src="src(c.a)" class="t" :style="{ width: `${size * 0.72}px`, left: '0px', top: '10px' }">
          <img :src="src(c.b)" class="t" :style="{ width: `${size * 0.72}px`, left: `${size * 0.72 + 14}px`, top: '10px' }">
          <div class="dt" :style="{ top: `${size * 0.72 + 18}px`, width: `${size * 1.44 + 14}px` }">
            <span v-if="c.kind === 'time'">Δt →</span><span v-else>Germany · Cambodia</span>
          </div>
        </template>
        <template v-else-if="c.kind === 'grid'">
          <div class="gridwrap" :style="{ width: `${size}px`, height: `${size}px`, left: '20px', top: '6px' }">
            <img :src="src(c.a)" class="t" :style="{ width: `${size}px`, left: 0, top: 0 }">
            <div class="grid" />
          </div>
        </template>
        <template v-else-if="c.kind === 'proc'">
          <img :src="src(c.a)" class="t" :style="{ width: `${size * 0.62}px`, left: '0px', top: '14px' }">
          <svg class="gear" :style="{ left: `${size * 0.62 + 6}px`, top: `${size * 0.31}px` }" width="30" height="30" viewBox="-15 -15 30 30">
            <g fill="none" stroke="var(--ink)" stroke-width="2.4">
              <circle r="5" /><circle r="9.5" />
              <line v-for="a in 8" :key="a" x1="0" y1="-9.5" x2="0" y2="-13.5" :transform="`rotate(${a * 45})`" />
            </g>
          </svg>
          <img :src="src(c.b)" class="t" :style="{ width: `${size * 0.62}px`, left: `${size * 0.62 + 42}px`, top: '14px' }">
        </template>
      </div>
      <div class="q">{{ c.q }}</div>
      <div class="note muted">{{ c.note }}</div>
      <div class="tag" :class="{ on: step >= tagAt }" :style="{ background: SHIFT_COLORS[c.shift], color: c.shift === 'Temporal' ? 'var(--ink)' : 'white', transitionDelay: `${i * 90}ms` }">
        {{ c.shift }} shift
      </div>
    </div>
  </div>
</template>

<style scoped>
.row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-top: 18px; }
.col { display: flex; flex-direction: column; align-items: center; text-align: center; opacity: 0; transform: translateY(12px); transition: opacity 450ms, transform 450ms cubic-bezier(.2,.7,.2,1); }
.col.on { opacity: 1; transform: none; }
.vis { position: relative; width: 160px; margin: 0 auto; }
.t { position: absolute; aspect-ratio: 1; object-fit: cover; border: 2px solid white; box-shadow: 0 1px 3px rgba(0,0,0,.25); }
.gridwrap { position: absolute; }
.grid {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,.85) 1.5px, transparent 1.5px), linear-gradient(90deg, rgba(255,255,255,.85) 1.5px, transparent 1.5px);
  background-size: 25% 25%;
}
.gear { position: absolute; }
.dt { position: absolute; left: 0; font-size: 12px; font-weight: 700; color: var(--muted); }
.q { font-weight: 700; font-size: 15px; margin-top: 6px; white-space: nowrap; }
.note { font-size: 12px; margin-top: 2px; margin-bottom: 8px; }
.tag {
  display: inline-block; margin-top: auto; padding: 2px 10px; border-radius: 999px; color: white; font-size: 13px; font-weight: 700;
  opacity: 0; transform: scale(.85); transition: opacity 350ms, transform 350ms;
}
.tag.on { opacity: 1; transform: none; }
</style>
