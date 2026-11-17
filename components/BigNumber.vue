<script setup lang="ts">
// Counts up to `value` once `step >= at`. Use for headline stats.
import { onUnmounted, ref, watch } from 'vue'

const props = withDefaults(defineProps<{
  value: number; suffix?: string; prefix?: string; label?: string
  step?: number; at?: number; duration?: number; decimals?: number; color?: string
}>(), { suffix: '', prefix: '', step: 99, at: 0, duration: 1200, decimals: 0, color: 'var(--ood)' })

const shown = ref(0)
let raf = 0
function run() {
  cancelAnimationFrame(raf)
  const t0 = performance.now()
  const tickFn = (t: number) => {
    const p = Math.min(1, (t - t0) / props.duration)
    shown.value = props.value * (1 - Math.pow(1 - p, 3))
    if (p < 1) raf = requestAnimationFrame(tickFn)
  }
  raf = requestAnimationFrame(tickFn)
}
watch(() => props.step >= props.at, (on) => { on ? run() : (shown.value = 0) }, { immediate: true })
onUnmounted(() => cancelAnimationFrame(raf))
</script>

<template>
  <div class="big" :style="{ opacity: step >= at ? 1 : 0.15 }">
    <div class="num" :style="{ color }">{{ prefix }}{{ shown.toFixed(decimals) }}{{ suffix }}</div>
    <div v-if="label" class="label">{{ label }}</div>
  </div>
</template>

<style scoped>
.big { text-align: center; transition: opacity 400ms; }
.num { font-size: 96px; font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; }
.label { margin-top: 8px; font-size: 16px; color: var(--muted); max-width: 260px; }
</style>
