<script setup lang="ts">
// Step-by-step explainer of effective robustness (Taori et al.; paper Sec 4.3).
// Models a, b, c are the paper's own worked example. The baseline line is
// ILLUSTRATIVE (OOD = 0.8·ID) — in the paper β is fit over all models per shift.
// Slide needs `clicks: 4`; pass :step="$clicks".
import { computed } from 'vue'
import nums from '../data/paper_numbers.json'
import { scale, ticks } from '../utils/csv'

const props = withDefaults(defineProps<{ step?: number; slope?: number; intercept?: number }>(),
  { step: 99, slope: 0.8, intercept: 0 })

const W = 560, H = 420, M = { l: 56, r: 20, t: 16, b: 48 }
const x = scale(0, 100, M.l, W - M.r)
const y = scale(0, 100, H - M.b, M.t)
const beta = (v: number) => props.slope * v + props.intercept
const models = nums.er_example.models
const tk = ticks(0, 100, 20)

const caption = computed(() => {
  if (props.step >= 4) return 'Effective robustness ρ = OOD − β(ID): distance above or below the baseline'
  if (props.step >= 3) return 'β(ID): the OOD score we would expect from a model with this ID score'
  if (props.step >= 2) return 'Ranking by the raw drop says b is more robust than a, but b is poor everywhere'
  if (props.step >= 1) return 'Three models from the paper: (a) 90 → 70, (b) 15 → 10, (c) 60 → 60'
  return 'Perfect robustness: OOD = ID'
})
const fmt = (v: number) => (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(Math.round(v * 10) / 10)
</script>

<template>
  <div class="er">
    <svg :viewBox="`0 0 ${W} ${H}`" :width="W" :height="H">
      <!-- grid + axes -->
      <g class="grid">
        <line v-for="t in tk" :key="'gx'+t" :x1="x(t)" :x2="x(t)" :y1="y(0)" :y2="y(100)" />
        <line v-for="t in tk" :key="'gy'+t" :x1="x(0)" :x2="x(100)" :y1="y(t)" :y2="y(t)" />
      </g>
      <g class="axis">
        <text v-for="t in tk" :key="'tx'+t" :x="x(t)" :y="H - M.b + 18" text-anchor="middle">{{ t }}</text>
        <text v-for="t in tk" :key="'ty'+t" :x="M.l - 8" :y="y(t) + 4" text-anchor="end">{{ t }}</text>
        <text :x="(M.l + W - M.r) / 2" :y="H - 6" text-anchor="middle" class="lab">ID score</text>
        <text :x="14" :y="(M.t + H - M.b) / 2" text-anchor="middle" class="lab" :transform="`rotate(-90 14 ${(M.t + H - M.b) / 2})`">OOD score</text>
      </g>

      <!-- y = x -->
      <line class="yx" :x1="x(0)" :y1="y(0)" :x2="x(100)" :y2="y(100)" />
      <text class="yx-lab" :x="x(78)" :y="y(86)">OOD = ID</text>

      <!-- naive gaps -->
      <g :class="['fade', { on: step >= 2 && step < 4 }]">
        <g v-for="m in models" :key="'g'+m.name">
          <line class="gap" :x1="x(m.id)" :x2="x(m.id)" :y1="y(m.id)" :y2="y(m.ood)" />
          <text class="gap-lab" :x="x(m.id) + 8" :y="y((m.id + m.ood) / 2) + 4">{{ fmt(m.ood - m.id) }}</text>
        </g>
      </g>

      <!-- baseline -->
      <g :class="['fade', { on: step >= 3 }]">
        <line class="beta" :x1="x(0)" :y1="y(beta(0))" :x2="x(100)" :y2="y(beta(100))" />
        <text class="beta-lab" :x="x(100) - 4" :y="y(beta(100)) + 18" text-anchor="end">β(ID) (illustrative)</text>
      </g>

      <!-- effective robustness -->
      <g :class="['fade', { on: step >= 4 }]">
        <g v-for="m in models" :key="'r'+m.name">
          <line class="rho" :class="{ pos: m.ood - beta(m.id) > 0 }" :x1="x(m.id)" :x2="x(m.id)" :y1="y(beta(m.id))" :y2="y(m.ood)" />
          <text class="rho-lab" :class="{ pos: m.ood - beta(m.id) > 0 }" :x="x(m.id) - 8" :y="y((beta(m.id) + m.ood) / 2) + 4" text-anchor="end">ρ {{ fmt(m.ood - beta(m.id)) }}</text>
        </g>
      </g>

      <!-- points -->
      <g :class="['fade', { on: step >= 1 }]">
        <g v-for="m in models" :key="'p'+m.name">
          <circle :cx="x(m.id)" :cy="y(m.ood)" r="8" class="pt" />
          <text :x="x(m.id)" :y="y(m.ood) - 14" text-anchor="middle" class="pt-lab">{{ m.name }}</text>
        </g>
      </g>
    </svg>
    <div class="caption">{{ caption }}</div>
  </div>
</template>

<style scoped>
.er { display: flex; flex-direction: column; align-items: center; }
.grid line { stroke: #eceef1; }
.axis text { font-size: 12px; fill: #6b7280; }
.axis .lab { font-size: 14px; fill: #374151; }
.yx { stroke: #d93a3a; stroke-width: 2.5; }
.yx-lab { fill: #d93a3a; font-size: 12px; font-weight: 700; }
.beta { stroke: #111; stroke-width: 2; stroke-dasharray: 7 5; }
.beta-lab { font-size: 12px; fill: #111; }
.gap { stroke: #9ca3af; stroke-width: 2; stroke-dasharray: 3 3; }
.gap-lab { font-size: 13px; fill: #6b7280; font-weight: 700; }
.rho { stroke: var(--ood); stroke-width: 3; }
.rho.pos { stroke: var(--id); }
.rho-lab { font-size: 13px; font-weight: 700; fill: var(--ood); }
.rho-lab.pos { fill: var(--id); }
.pt { fill: #1f2328; }
.pt-lab { font-weight: 700; font-size: 15px; }
.fade { opacity: 0; transition: opacity 500ms ease; }
.fade.on { opacity: 1; }
.caption { min-height: 1.6em; font-size: 16px; margin-top: 4px; text-align: center; }
</style>
