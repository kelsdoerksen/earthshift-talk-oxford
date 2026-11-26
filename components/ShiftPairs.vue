<script setup lang="ts">
import { asset } from '../utils/asset'
// The five EarthShift shift types as static ID → OOD pairs (no looping), one column per click (step >= i + 1).
// Tiles from public/tiles (paper Fig. 1); shift names in SHIFT_COLORS.
import { SHIFT_COLORS } from '../utils/csv'

const props = withDefaults(defineProps<{ step?: number; size?: number }>(), { step: 99, size: 118 })

const shifts = [
  { name: 'Scale', what: 'resolution changes', id: 'resisc45_baseball_id', ood: 'ucmerced_baseball_ood', idc: 'RESISC45 (0.2–30 m)', oodc: 'UCMerced (0.3 m)' },
  { name: 'Temporal', what: 'acquisition time changes', id: 'rpg_2017_id', ood: 'rpg_2022_ood', idc: 'France RPG 2017', oodc: 'France RPG 2022' },
  { name: 'Geographic', what: 'location changes', id: 'ftw_germany_image_id', ood: 'ftw_cambodia_image_ood', idc: 'FTW Germany', oodc: 'FTW Cambodia' },
  { name: 'Sensor', what: 'imaging sensor changes', id: 'sen1floods11_s2_id', ood: 'sen1floods11_s1_ood', idc: 'Sentinel-2 (optical)', oodc: 'Sentinel-1 (SAR)' },
  { name: 'Processing', what: 'processing level changes', id: 'cloudsen12_l2a_id', ood: 'cloudsen12_l1c_ood', idc: 'CloudSen12 L2A', oodc: 'CloudSen12 L1C' },
]
</script>

<template>
  <div class="pairs">
    <div v-for="(s, i) in shifts" :key="s.name" class="col" :class="{ on: step >= i + 1 }">
      <div class="name" :style="{ color: SHIFT_COLORS[s.name] }">{{ s.name }}</div>
      <div class="what muted">{{ s.what }}</div>
      <img :src="asset(`/tiles/${s.id}.png`)" :width="size" :height="size" :alt="`${s.idc} (ID)`">
      <div class="cap id">{{ s.idc }}</div>
      <svg width="24" height="30" viewBox="0 0 24 30" class="down"><path d="M12 2 V24 M4 17 L12 27 L20 17" fill="none" :stroke="SHIFT_COLORS[s.name]" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
      <img :src="asset(`/tiles/${s.ood}.png`)" :width="size" :height="size" :alt="`${s.oodc} (OOD)`">
      <div class="cap ood">{{ s.oodc }}</div>
    </div>
  </div>
</template>

<style scoped>
.pairs { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 8px; }
.col { display: flex; flex-direction: column; align-items: center; text-align: center; opacity: 0; transition: opacity 450ms; }
.col.on { opacity: 1; }
.name { font-weight: 700; font-size: 18px; }
.what { font-size: 12px; margin-bottom: 6px; }
img { object-fit: cover; display: block; }
.cap { font-size: 12px; margin-top: 3px; }
.down { margin: 2px 0 1px; }
</style>
