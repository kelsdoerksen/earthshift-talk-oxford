<script setup lang="ts">
// "Does the best ID model stay the best OOD model?" Kendall τ per shift (paper p.7 / Fig 2).
// Bars grow one per click in order of decreasing τ. Slide: `clicks: 5`, :step="$clicks".
import { computed } from 'vue'
import nums from '../data/paper_numbers.json'
import { SHIFT_COLORS } from '../utils/csv'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 99 })
const raw = nums.kendall_tau as Record<string, number | string>
const rows = computed(() => Object.entries(raw)
  .filter(([k]) => !k.startsWith('_'))
  .map(([k, v]) => ({ name: k, tau: v as number }))
  .sort((a, b) => b.tau - a.tau)
  .map((r, i) => ({ ...r, on: props.step >= i + 1 })))

const lo = -0.25, hi = 1
const pct = (v: number) => ((v - lo) / (hi - lo)) * 100
const zero = pct(0)
</script>

<template>
  <div class="tau">
    <div v-for="r in rows" :key="r.name" class="row">
      <div class="name">{{ r.name }}</div>
      <div class="track">
        <div class="zero" :style="{ left: zero + '%' }" />
        <div
          class="bar"
          :style="{
            left: (r.tau >= 0 ? zero : pct(r.tau)) + '%',
            width: (r.on ? Math.abs(pct(r.tau) - zero) : 0) + '%',
            background: SHIFT_COLORS[r.name],
          }"
        />
        <div class="val" :style="{ left: (r.tau >= 0 ? pct(r.tau) : zero) + '%', opacity: r.on ? 1 : 0 }">
          τ = {{ r.tau.toFixed(2) }}
        </div>
      </div>
    </div>
    <div class="scale muted">
      <span :style="{ left: zero + '%' }">0 · rankings unrelated</span>
      <span :style="{ left: pct(1) + '%' }">1 · same ranking</span>
    </div>
  </div>
</template>

<style scoped>
.tau { width: 640px; margin: 10px auto 0; }
.row { display: flex; align-items: center; height: 46px; }
.name { width: 110px; font-weight: 700; font-size: 16px; }
.track { position: relative; flex: 1; height: 26px; }
.zero { position: absolute; top: -6px; bottom: -6px; width: 2px; background: #9ca3af; }
.bar { position: absolute; top: 0; height: 100%; border-radius: 3px; transition: width 800ms cubic-bezier(.2,.7,.2,1); }
.val { position: absolute; top: 3px; margin-left: 8px; font-size: 14px; font-weight: 700; white-space: nowrap; transition: opacity 400ms 500ms; }
.scale { position: relative; margin-left: 110px; height: 22px; font-size: 11px; }
.scale span { position: absolute; transform: translateX(-50%); white-space: nowrap; }
</style>
