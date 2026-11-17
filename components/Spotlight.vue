<script setup lang="ts">
// Shows a static figure and dims everything except one region per click.
// spots: [{ x, y, w, h, at, label }] in % of the image box; the spot with the
// largest `at` <= step is shown. Great for walking through paper figures.
import { computed } from 'vue'

interface Spot { x: number; y: number; w: number; h: number; at: number; label?: string }
const props = withDefaults(defineProps<{ src: string; spots?: Spot[]; step?: number; width?: string }>(),
  { spots: () => [], step: 0, width: '100%' })

const active = computed(() => [...props.spots].filter(s => s.at <= props.step).sort((a, b) => b.at - a.at)[0])
</script>

<template>
  <div class="spot-wrap" :style="{ width }">
    <img :src="src" class="fig" alt="">
    <div
      v-if="active" class="spot"
      :style="{ left: active.x + '%', top: active.y + '%', width: active.w + '%', height: active.h + '%' }"
    >
      <div v-if="active.label" class="spot-label">{{ active.label }}</div>
    </div>
  </div>
</template>

<style scoped>
.spot-wrap { position: relative; overflow: hidden; margin: 0 auto; }
.fig { display: block; width: 100%; }
.spot {
  position: absolute; border-radius: 10px; border: 3px solid var(--ood);
  box-shadow: 0 0 0 9999px rgba(15, 18, 24, 0.55);
  transition: all 600ms cubic-bezier(.2,.7,.2,1);
}
.spot-label {
  position: absolute; top: 100%; left: 0; margin-top: 8px; white-space: nowrap;
  background: var(--ood); color: white; font-weight: 700; font-size: 14px; padding: 3px 8px; border-radius: 4px;
}
</style>
