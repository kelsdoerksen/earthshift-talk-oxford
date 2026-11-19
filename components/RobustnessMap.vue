<script setup lang="ts">
// Animated version of Fig 3: overall OOD score (x) vs effective robustness (y), one dot per model.
// Reads data/model_summary.csv (make it with scripts/export_results.py).
// Clicks: 1 = GFMs, 2 = generic pretrained, 3 = random init. Slide: `clicks: 3`.
import { computed } from 'vue'
import raw from '../data/model_summary.csv?raw'
import { parseCsv, scale, ticks, FAMILY_COLORS } from '../utils/csv'

const props = withDefaults(defineProps<{ protocol?: 'FULL' | 'HEAD'; shift?: string; step?: number; title?: string; legend?: boolean; width?: number }>(),
  { protocol: 'FULL', shift: 'Overall', step: 99, legend: true, width: 640 })
// display names as in paper Fig. 3
const LABEL: Record<string, string> = {
  clay: 'Clay', croma: 'CROMA', dofa: 'DOFA', prithvi: 'Prithvi-2.0', terrafm: 'TerraFM', terramind: 'TerraMind',
  dinov3_large_sat: 'DINOv3', clip: 'CLIP', resnet50_imgnet: 'R50-imgnet', vit_imgnet: 'ViT-imgnet',
  resnet_random: 'R50-rnd', vit_random: 'ViT-rnd',
}

const ORDER = ['GFM', 'VFM', 'Random']
const NAMES: Record<string, string> = { GFM: 'Geospatial FM', VFM: 'Generic pretrained', Random: 'Random init' }
const rows = computed(() => parseCsv(raw)
  .filter(r => r.protocol === props.protocol && r.shift === props.shift)
  .map(r => ({ model: r.model, family: r.family, ood: +r.ood, er: +r.er })))

const W = 640, H = 420, M = { l: 60, r: 20, t: 28, b: 70 }
const dom = computed(() => {
  const xs = rows.value.map(r => r.ood), ys = rows.value.map(r => r.er)
  const pad = (a: number, b: number) => { const p = (b - a) * 0.12 || 1; return [a - p, b + p] }
  return { x: pad(Math.min(...xs), Math.max(...xs)), y: pad(Math.min(...ys, 0), Math.max(...ys, 0)) }
})
const x = computed(() => scale(dom.value.x[0], dom.value.x[1], M.l, W - M.r))
const y = computed(() => scale(dom.value.y[0], dom.value.y[1], H - M.b, M.t))
const niceStep = (span: number) => [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 2.5, 5, 10].find(s => span / s <= 7) ?? 20
const xt = computed(() => ticks(dom.value.x[0], dom.value.x[1], niceStep(dom.value.x[1] - dom.value.x[0])))
const yt = computed(() => ticks(dom.value.y[0], dom.value.y[1], niceStep(dom.value.y[1] - dom.value.y[0])))
// greedy label placement: try right-up, right-down, left-up, left-down; keep the first that overlaps no label or dot
const labels = computed(() => {
  const boxes: number[][] = rows.value.map(r => [x.value(r.ood) - 8, y.value(r.er) - 8, x.value(r.ood) + 8, y.value(r.er) + 8])
  const hit = (b: number[]) => boxes.some(o => b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1])
  const out: Record<string, { x: number; y: number; anchor: string }> = {}
  ;[...rows.value].sort((a, b) => b.er - a.er).forEach((r) => {
    const name = LABEL[r.model] ?? r.model, w = name.length * 7.2 + 4, h = 14, cx = x.value(r.ood), cy = y.value(r.er)
    const cands = [[cx + 10, cy - 8, 'start'], [cx + 10, cy + 18, 'start'], [cx - 10, cy - 8, 'end'], [cx - 10, cy + 18, 'end'], [cx + 10, cy + 4, 'start'], [cx - 10, cy + 4, 'end']] as [number, number, string][]
    let pick = cands[0]
    for (const c of cands) {
      const x0 = c[2] === 'start' ? c[0] : c[0] - w
      const b = [x0, c[1] - h + 3, x0 + w, c[1] + 3]
      if (!hit(b) && b[0] > M.l && b[2] < W - M.r) { pick = c; break }
    }
    const x0 = pick[2] === 'start' ? pick[0] : pick[0] - w
    boxes.push([x0, pick[1] - h + 3, x0 + w, pick[1] + 3])
    out[r.model] = { x: pick[0], y: pick[1], anchor: pick[2] }
  })
  return out
})
const shownFam = (f: string) => props.step >= ORDER.indexOf(f) + 1 || ORDER.indexOf(f) < 0
</script>

<template>
  <div v-if="!rows.length" class="empty">
    <div class="kicker">No data yet</div>
    <p>Run <code>python3 scripts/export_results.py full.csv:FULL head.csv:HEAD</code> to fill <code>data/model_summary.csv</code>.</p>
    <p class="muted small">Until then, use the paper figure with &lt;Spotlight&gt;.</p>
  </div>
  <svg v-else :viewBox="`0 0 ${W} ${legend ? H : H - 22}`" :width="width" class="rmap">
    <text v-if="title" :x="M.l" y="16" class="ptitle">{{ title }}</text>
    <g class="gridlines">
      <line v-for="t in xt" :key="'gx'+t" :x1="x(t)" :x2="x(t)" :y1="M.t" :y2="H - M.b" />
      <line v-for="t in yt" :key="'gy'+t" :x1="M.l" :x2="W - M.r" :y1="y(t)" :y2="y(t)" />
    </g>
    <line class="zero" :x1="M.l" :x2="W - M.r" :y1="y(0)" :y2="y(0)" />
    <g class="axis">
      <text v-for="t in xt" :key="'tx'+t" :x="x(t)" :y="H - M.b + 18" text-anchor="middle">{{ t }}</text>
      <text v-for="t in yt" :key="'ty'+t" :x="M.l - 8" :y="y(t) + 4" text-anchor="end">{{ t }}</text>
      <text :x="(M.l + W - M.r) / 2" :y="H - M.b + 40" text-anchor="middle" class="lab">{{ shift }} OOD score</text>
      <text x="16" :y="(M.t + H - M.b) / 2" text-anchor="middle" class="lab" :transform="`rotate(-90 16 ${(M.t + H - M.b) / 2})`">Effective robustness</text>
    </g>
    <g v-for="r in rows" :key="r.model" class="dot" :style="{ opacity: shownFam(r.family) ? 1 : 0, transform: shownFam(r.family) ? 'none' : 'translateY(12px)' }">
      <circle :cx="x(r.ood)" :cy="y(r.er)" r="7" :fill="FAMILY_COLORS[r.family] || '#888'" />
      <text :x="labels[r.model].x" :y="labels[r.model].y" :text-anchor="labels[r.model].anchor" class="name">{{ LABEL[r.model] ?? r.model }}</text>
    </g>
    <g v-if="legend" class="legend">
      <g v-for="(f, i) in ORDER" :key="f" :transform="`translate(${M.l + i * 170}, ${H - 12})`" :style="{ opacity: shownFam(f) ? 1 : 0.25 }">
        <circle r="6" :fill="FAMILY_COLORS[f]" /><text x="12" y="4">{{ NAMES[f] }}</text>
      </g>
    </g>
  </svg>
</template>

<style scoped>
.gridlines line { stroke: #eceef1; }
.zero { stroke: #6b7280; stroke-dasharray: 5 4; }
.axis text { font-size: 12px; fill: #6b7280; }
.axis .lab { font-size: 14px; fill: #374151; }
.dot { transition: opacity 500ms ease, transform 500ms ease; }
.name { font-size: 12px; font-weight: 700; }
.ptitle { font-size: 15px; font-weight: 700; fill: #1f2328; }
.rmap { display: block; height: auto; }
.legend text { font-size: 13px; }
.empty { border: 2px dashed var(--rule); border-radius: 10px; padding: 24px 28px; max-width: 560px; margin: 30px auto; }
</style>
