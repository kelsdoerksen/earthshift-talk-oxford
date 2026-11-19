<script setup lang="ts">
// The five per-shift linear fits from Fig 2 (frozen fine-tuning), drawn one per click.
// Lines below the red y = x line mean models lose performance OOD.
// Slide needs `clicks: 5`; pass :step="$clicks".
import { computed } from 'vue'
import nums from '../data/paper_numbers.json'
import { scale, ticks, SHIFT_COLORS } from '../utils/csv'

const props = withDefaults(defineProps<{ step?: number; order?: string[]; showTau?: boolean }>(), {
  step: 99,
  order: () => ['Temporal', 'Scale', 'Geographic', 'Processing', 'Sensor'],
  showTau: true,
})

const W = 620, H = 430, M = { l: 56, r: 150, t: 16, b: 48 }
const x = scale(0.2, 1.0, M.l, W - M.r)
const y = scale(0.0, 1.0, H - M.b, M.t)
const fits = nums.fits_frozen as Record<string, { m: number; b: number; x_range: number[] }>
const tau = nums.kendall_tau as Record<string, number>

const lines = computed(() => props.order.map((name, i) => {
  const f = fits[name]
  const [x0, x1] = f.x_range
  const len = Math.hypot(x(x1) - x(x0), y(f.m * x1 + f.b) - y(f.m * x0 + f.b))
  return { name, i, f, x0, x1, len, color: SHIFT_COLORS[name], on: props.step >= i + 1 }
}))
const sign = (v: number) => (v < 0 ? '− ' : '+ ') + Math.abs(v).toFixed(3)
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" class="fits">
    <g class="gridlines">
      <line v-for="t in ticks(0.2, 1, 0.1)" :key="'gx'+t" :x1="x(t)" :x2="x(t)" :y1="y(0)" :y2="y(1)" />
      <line v-for="t in ticks(0, 1, 0.1)" :key="'gy'+t" :x1="x(0.2)" :x2="x(1)" :y1="y(t)" :y2="y(t)" />
    </g>
    <g class="axis">
      <text v-for="t in ticks(0.2, 1, 0.2)" :key="'tx'+t" :x="x(t)" :y="H - M.b + 18" text-anchor="middle">{{ t.toFixed(1) }}</text>
      <text v-for="t in ticks(0, 1, 0.2)" :key="'ty'+t" :x="M.l - 8" :y="y(t) + 4" text-anchor="end">{{ t.toFixed(1) }}</text>
      <text :x="(M.l + W - M.r) / 2" :y="H - 6" text-anchor="middle" class="lab">In-distribution score</text>
      <text x="14" :y="(M.t + H - M.b) / 2" text-anchor="middle" class="lab" :transform="`rotate(-90 14 ${(M.t + H - M.b) / 2})`">Out-of-distribution score</text>
    </g>

    <line class="yx" :x1="x(0.2)" :y1="y(0.2)" :x2="x(1)" :y2="y(1)" />
    <text class="yx-lab" :x="x(0.84)" :y="y(0.93)">no degradation</text>

    <g v-for="l in lines" :key="l.name">
      <line
        :x1="x(l.x0)" :y1="y(l.f.m * l.x0 + l.f.b)" :x2="x(l.x1)" :y2="y(l.f.m * l.x1 + l.f.b)"
        :stroke="l.color" stroke-width="4" stroke-linecap="round"
        :style="{ strokeDasharray: l.len, strokeDashoffset: l.on ? 0 : l.len, transition: 'stroke-dashoffset 900ms ease' }"
      />
      <g :style="{ opacity: l.on ? 1 : 0, transition: 'opacity 400ms 600ms' }">
        <text :x="W - M.r + 10" :y="M.t + 22 + l.i * 52" :fill="l.color" class="leg">{{ l.name }}</text>
        <text :x="W - M.r + 10" :y="M.t + 38 + l.i * 52" class="leg-sub">{{ l.f.m.toFixed(3) }}·ID {{ sign(l.f.b) }}</text>
        <text v-if="showTau" :x="W - M.r + 10" :y="M.t + 52 + l.i * 52" class="leg-sub">τ = {{ tau[l.name].toFixed(2) }}</text>
      </g>
    </g>
  </svg>
</template>

<style scoped>
.fits { display: block; max-height: 400px; }
.gridlines line { stroke: #eceef1; }
.axis text { font-size: 12px; fill: #6b7280; }
.axis .lab { font-size: 14px; fill: #374151; }
.yx { stroke: #d93a3a; stroke-width: 2; stroke-dasharray: 6 4; }
.yx-lab { fill: #d93a3a; font-size: 12px; font-weight: 700; }
.leg { font-weight: 700; font-size: 15px; }
.leg-sub { font-size: 11px; fill: #4b5563; font-family: ui-monospace, Menlo, monospace; }
</style>
