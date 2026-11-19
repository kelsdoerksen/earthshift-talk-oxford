<script setup lang="ts">
// ID -> OOD slope chart for one shift + protocol: every model's line "falls" when you click.
// Click 1: ID scores appear. Click 2: lines drop to OOD. Click 3: highlight `highlight` models.
// Reads data/model_summary.csv. Slide: `clicks: 3`.
import { computed } from 'vue'
import raw from '../data/model_summary.csv?raw'
import { parseCsv, scale, FAMILY_COLORS } from '../utils/csv'

const props = withDefaults(defineProps<{
  shift?: string; protocol?: 'FULL' | 'HEAD'; step?: number; highlight?: string[]; title?: string
}>(), { shift: 'Overall', protocol: 'FULL', step: 99, highlight: () => [] })

const rows = computed(() => parseCsv(raw)
  .filter(r => r.protocol === props.protocol && r.shift === props.shift)
  .map(r => ({ model: r.model, family: r.family, id: +r.id, ood: +r.ood })))

const W = 640, H = 450, M = { l: 200, r: 200, t: 34, b: 20 }
const LABEL: Record<string, string> = {
  clay: 'Clay', croma: 'CROMA', dofa: 'DOFA', prithvi: 'Prithvi-2.0', terrafm: 'TerraFM', terramind: 'TerraMind',
  dinov3_large_sat: 'DINOv3', clip: 'CLIP', resnet50_imgnet: 'R50-imgnet', vit_imgnet: 'ViT-imgnet',
  resnet_random: 'R50-rnd', vit_random: 'ViT-rnd',
}
const name = (m: string) => LABEL[m] ?? m
// spread labels on one side so none overlap: keep order, enforce a minimum gap, then fit inside the plot
const GAP = 17
function spread(ys: { k: string; y: number }[]) {
  const s = [...ys].sort((a, b) => a.y - b.y), out: Record<string, number> = {}
  let prev = -Infinity
  for (const p of s) { const v = Math.max(p.y, prev + GAP); out[p.k] = v; prev = v }
  const over = prev - (H - M.b)
  if (over > 0) { let next = Infinity; for (const p of [...s].reverse()) { out[p.k] = Math.min(out[p.k] - over, next - GAP); next = out[p.k] } }
  return out
}
const dom = computed(() => {
  const v = rows.value.flatMap(r => [r.id, r.ood])
  const hi = Math.max(...v), lo = Math.min(...v)
  const unit = hi > 1.5 ? 10 : 0.1
  return [Math.floor(lo / unit) * unit, Math.ceil(hi / unit) * unit, unit] as const
})
const y = computed(() => scale(dom.value[0], dom.value[1], H - M.b, M.t))
const xl = M.l, xr = W - M.r
const labL = computed(() => spread(rows.value.map(r => ({ k: r.model, y: y.value(r.id) }))))
const labR = computed(() => spread(rows.value.map(r => ({ k: r.model, y: y.value(r.ood) }))))
const dim = (m: string) => props.step >= 3 && props.highlight.length && !props.highlight.includes(m)
const len = (r: { id: number; ood: number }) => Math.hypot(xr - xl, y.value(r.ood) - y.value(r.id))
const fmt = (v: number) => (dom.value[2] === 10 ? v.toFixed(1) : v.toFixed(3))
</script>

<template>
  <div v-if="!rows.length" class="empty">
    <div class="kicker">No data yet for {{ shift }} · {{ protocol }}</div>
    <p>Fill <code>data/model_summary.csv</code> with <code>scripts/export_results.py</code>.</p>
  </div>
  <svg v-else :viewBox="`0 0 ${W} ${H}`" :width="W" style="display: block; height: auto; max-height: 420px">
    <line class="axisline" :x1="xl" :x2="xl" :y1="M.t" :y2="H - M.b" />
    <line class="axisline" :x1="xr" :x2="xr" :y1="M.t" :y2="H - M.b" />
    <text :x="xl" :y="M.t - 12" text-anchor="middle" class="head id">ID</text>
    <text :x="xr" :y="M.t - 12" text-anchor="middle" class="head ood">OOD</text>

    <g v-for="r in rows" :key="r.model" :style="{ opacity: step >= 1 ? (dim(r.model) ? 0.15 : 1) : 0, transition: 'opacity 500ms' }">
      <line
        :x1="xl" :y1="y(r.id)" :x2="xr" :y2="y(r.ood)"
        :stroke="FAMILY_COLORS[r.family]" stroke-width="2.5" class="seg"
        :style="{ strokeDasharray: len(r), strokeDashoffset: step >= 2 ? 0 : len(r) }"
      />
      <circle :cx="xl" :cy="y(r.id)" r="5" :fill="FAMILY_COLORS[r.family]" />
      <path :d="`M${xl - 7},${y(r.id)} L${xl - 30},${labL[r.model]}`" class="leader" :stroke="FAMILY_COLORS[r.family]" />
      <text :x="xl - 34" :y="labL[r.model] + 4" text-anchor="end" class="lab" :fill="FAMILY_COLORS[r.family]">
        <tspan class="nm">{{ name(r.model) }}</tspan> <tspan class="val">{{ fmt(r.id) }}</tspan></text>
      <g :style="{ opacity: step >= 2 ? 1 : 0, transition: 'opacity 400ms 500ms' }">
        <circle :cx="xr" :cy="y(r.ood)" r="5" :fill="FAMILY_COLORS[r.family]" />
        <path :d="`M${xr + 7},${y(r.ood)} L${xr + 30},${labR[r.model]}`" class="leader" :stroke="FAMILY_COLORS[r.family]" />
        <text :x="xr + 34" :y="labR[r.model] + 4" class="lab" :fill="FAMILY_COLORS[r.family]">
          <tspan class="val">{{ fmt(r.ood) }}</tspan> <tspan class="nm">{{ name(r.model) }}</tspan></text>
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
.lab { font-size: 13px; }
.nm { font-weight: 700; }
.val { fill: #4b5563; font-weight: 400; }
.leader { stroke-width: 1; fill: none; opacity: 0.6; }
.seg { transition: stroke-dashoffset 900ms cubic-bezier(.2,.7,.2,1); }
.empty { border: 2px dashed var(--rule); border-radius: 10px; padding: 24px 28px; max-width: 560px; margin: 30px auto; }
</style>
