<script setup lang="ts">
// ID -> OOD slope chart for one shift + protocol: every model's line "falls" when you click.
// Click 1: ID scores appear. Click 2: lines drop to OOD. Click 3: highlight `highlight` models.
// Reads data/model_summary.csv. Slide: `clicks: 3`.
import { computed } from 'vue'
import raw from '../data/model_summary.csv?raw'
import { parseCsv, scale, ticks, FAMILY_COLORS } from '../utils/csv'

const props = withDefaults(defineProps<{
  shift?: string; protocol?: 'FULL' | 'HEAD'; step?: number; highlight?: string[]; title?: string
}>(), { shift: 'Overall', protocol: 'FULL', step: 99, highlight: () => [] })

const rows = computed(() => parseCsv(raw)
  .filter(r => r.protocol === props.protocol && r.shift === props.shift)
  .map(r => ({ model: r.model, family: r.family, id: +r.id, ood: +r.ood })))

const W = 560, H = 440, M = { l: 160, r: 160, t: 30, b: 40 }
const dom = computed(() => {
  const v = rows.value.flatMap(r => [r.id, r.ood])
  const hi = Math.max(...v), lo = Math.min(...v)
  const unit = hi > 1.5 ? 10 : 0.1
  return [Math.floor(lo / unit) * unit, Math.ceil(hi / unit) * unit, unit] as const
})
const y = computed(() => scale(dom.value[0], dom.value[1], H - M.b, M.t))
const xl = M.l, xr = W - M.r
const dim = (m: string) => props.step >= 3 && props.highlight.length && !props.highlight.includes(m)
const len = (r: { id: number; ood: number }) => Math.hypot(xr - xl, y.value(r.ood) - y.value(r.id))
const fmt = (v: number) => (dom.value[2] === 10 ? v.toFixed(1) : v.toFixed(3))
</script>

<template>
  <div v-if="!rows.length" class="empty">
    <div class="kicker">No data yet for {{ shift }} · {{ protocol }}</div>
    <p>Fill <code>data/model_summary.csv</code> with <code>scripts/export_results.py</code>.</p>
  </div>
  <svg v-else :viewBox="`0 0 ${W} ${H}`" :width="W" :height="H">
    <line class="axisline" :x1="xl" :x2="xl" :y1="M.t" :y2="H - M.b" />
    <line class="axisline" :x1="xr" :x2="xr" :y1="M.t" :y2="H - M.b" />
    <text :x="xl" :y="M.t - 12" text-anchor="middle" class="head id">ID</text>
    <text :x="xr" :y="M.t - 12" text-anchor="middle" class="head ood">OOD</text>
    <text v-for="t in ticks(dom[0], dom[1], dom[2])" :key="t" :x="(xl + xr) / 2" :y="y(t) + 4" text-anchor="middle" class="tick">{{ dom[2] === 10 ? t : t.toFixed(1) }}</text>

    <g v-for="r in rows" :key="r.model" :style="{ opacity: step >= 1 ? (dim(r.model) ? 0.15 : 1) : 0, transition: 'opacity 500ms' }">
      <line
        :x1="xl" :y1="y(r.id)" :x2="xr" :y2="y(r.ood)"
        :stroke="FAMILY_COLORS[r.family]" stroke-width="2.5" class="seg"
        :style="{ strokeDasharray: len(r), strokeDashoffset: step >= 2 ? 0 : len(r) }"
      />
      <circle :cx="xl" :cy="y(r.id)" r="5" :fill="FAMILY_COLORS[r.family]" />
      <text :x="xl - 10" :y="y(r.id) + 4" text-anchor="end" class="lab">{{ r.model }} {{ fmt(r.id) }}</text>
      <g :style="{ opacity: step >= 2 ? 1 : 0, transition: 'opacity 400ms 500ms' }">
        <circle :cx="xr" :cy="y(r.ood)" r="5" :fill="FAMILY_COLORS[r.family]" />
        <text :x="xr + 10" :y="y(r.ood) + 4" class="lab">{{ fmt(r.ood) }} {{ r.model }}</text>
      </g>
    </g>
  </svg>
</template>

<style scoped>
.axisline { stroke: #d6d9de; stroke-width: 2; }
.head { font-weight: 800; font-size: 16px; }
.head.id { fill: var(--id); }
.head.ood { fill: var(--ood); }
.tick { font-size: 10px; fill: #b0b5bc; }
.lab { font-size: 11px; }
.seg { transition: stroke-dashoffset 900ms cubic-bezier(.2,.7,.2,1); }
.empty { border: 2px dashed var(--rule); border-radius: 10px; padding: 24px 28px; max-width: 560px; margin: 30px auto; }
</style>
