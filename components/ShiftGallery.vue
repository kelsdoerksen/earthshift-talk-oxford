<script setup lang="ts">
// The five EarthShift shift types; each card loops ID <-> OOD.
// Cards appear one per click: pass :step="$clicks" and set `clicks: 5` on the slide.
const props = withDefaults(defineProps<{ step?: number; size?: number }>(), { step: 99, size: 150 })

const shifts = [
  { name: 'Scale', what: 'resolution changes', id: 'resisc45_baseball_id', ood: 'ucmerced_baseball_ood', idc: 'RESISC45 (0.2–30 m)', oodc: 'UCMerced (0.3 m)' },
  { name: 'Temporal', what: 'acquisition time changes', id: 'rpg_2017_id', ood: 'rpg_2022_ood', idc: 'France RPG 2017', oodc: 'France RPG 2022' },
  { name: 'Geographic', what: 'location changes', id: 'ftw_germany_image_id', ood: 'ftw_cambodia_image_ood', idc: 'FTW Germany', oodc: 'FTW Cambodia' },
  { name: 'Sensor', what: 'imaging sensor changes', id: 'sen1floods11_s2_id', ood: 'sen1floods11_s1_ood', idc: 'Sentinel-2', oodc: 'Sentinel-1' },
  { name: 'Processing', what: 'processing level changes', id: 'cloudsen12_l2a_id', ood: 'cloudsen12_l1c_ood', idc: 'CloudSen12 L2A', oodc: 'CloudSen12 L1C' },
]
</script>

<template>
  <div class="gallery">
    <div
      v-for="(s, i) in shifts" :key="s.name"
      class="card" :class="{ shown: props.step >= i + 1 || props.step >= 99 }"
    >
      <div class="name">{{ s.name }}</div>
      <div class="what muted">{{ s.what }}</div>
      <IdOodSwap mode="auto" :interval="2000 + i * 150" :id="s.id" :ood="s.ood" :id-caption="s.idc" :ood-caption="s.oodc" :size="size" />
    </div>
  </div>
</template>

<style scoped>
.gallery { display: flex; gap: 18px; justify-content: center; margin-top: 18px; }
.card { opacity: 0; transform: translateY(16px); transition: all 500ms cubic-bezier(.2,.7,.2,1); text-align: center; }
.card.shown { opacity: 1; transform: none; }
.name { font-weight: 700; font-size: 18px; }
.what { font-size: 12px; margin-bottom: 8px; }
</style>
