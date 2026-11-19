<script setup lang="ts">
// A 2-D sketch of embedding space, after Hannah Kerner's "Evaluating a model on a dataset" slide.
// mode: 'raw'      labelled examples as dots, plus one new image (ring)
//       'knn'      a circle reaches the new image's k nearest labelled neighbours
//       'linear'   frozen backbone: class regions are drawn over the SAME dots; dots on the wrong side get a ring
//       'finetune' the backbone changes, so the dots themselves move into tighter groups
// ILLUSTRATION ONLY: synthetic points from a fixed seed. No numbers on this panel are results.
import { computed } from 'vue'

type Mode = 'raw' | 'knn' | 'linear' | 'finetune'
const props = withDefaults(defineProps<{ mode?: Mode; width?: number; k?: number }>(),
  { mode: 'finetune', width: 300, k: 5 })

const W = 300, H = 260
const classes = [
  { name: 'maize', color: '#c9a227', c: [82, 88] },
  { name: 'wheat', color: '#8c6d46', c: [222, 92] },
  { name: 'peas', color: '#5a9e4b', c: [150, 196] },
]
// seeded RNG (mulberry32) + Box-Muller, so the sketch is identical every time
function rng(seed: number) {
  return () => { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296 }
}
const rand = rng(20261117)
const gauss = () => Math.sqrt(-2 * Math.log(rand() + 1e-9)) * Math.cos(2 * Math.PI * rand())
const SPREAD = 40, TIGHT = 0.4
const pts = classes.flatMap((cl, ci) => Array.from({ length: 13 }, () => {
  const clamp = (v: number, hi: number) => Math.min(hi - 12, Math.max(12, v))
  const x = clamp(cl.c[0] + gauss() * SPREAD, W), y = clamp(cl.c[1] + gauss() * SPREAD * 0.85, H)
  return { ci, raw: [x, y], ft: [cl.c[0] + (x - cl.c[0]) * TIGHT, cl.c[1] + (y - cl.c[1]) * TIGHT] }
}))
// the new image: a maize field that sits between maize and peas in the frozen embedding
const query = { ci: 0, raw: [118, 140], ft: [82 + (118 - 82) * TIGHT, 88 + (140 - 88) * TIGHT] }

const nearest = (p: number[]) => {
  let best = 0, bd = Infinity
  classes.forEach((cl, i) => { const d = (p[0] - cl.c[0]) ** 2 + (p[1] - cl.c[1]) ** 2; if (d < bd) { bd = d; best = i } })
  return best
}
const ft = computed(() => props.mode === 'finetune')
const pos = (p: { raw: number[]; ft: number[] }) => (ft.value ? p.ft : p.raw)

// k-NN in the frozen embedding
const knn = computed(() => {
  const d = pts.map((p, i) => ({ i, d: Math.hypot(p.raw[0] - query.raw[0], p.raw[1] - query.raw[1]) })).sort((a, b) => a.d - b.d)
  return { ids: new Set(d.slice(0, props.k).map(x => x.i)), r: d[props.k - 1].d + 9 }
})
// linear regions: nearest class centre (a linear classifier). Each region is the panel clipped by the
// half-planes "closer to my centre than to centre j" (Sutherland-Hodgman), so the borders are straight lines.
function clip(poly: number[][], a: number[], b: number[]) {
  // keep points p with |p-a|^2 <= |p-b|^2, i.e. n·p <= k
  const n = [b[0] - a[0], b[1] - a[1]], k = (b[0] ** 2 + b[1] ** 2 - a[0] ** 2 - a[1] ** 2) / 2
  const side = (p: number[]) => n[0] * p[0] + n[1] * p[1] - k
  const out: number[][] = []
  poly.forEach((p, i) => {
    const q = poly[(i + 1) % poly.length], sp = side(p), sq = side(q)
    if (sp <= 0) out.push(p)
    if ((sp < 0 && sq > 0) || (sp > 0 && sq < 0)) { const t = sp / (sp - sq); out.push([p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])]) }
  })
  return out
}
const regions = classes.map((cl, i) => {
  let poly = [[0, 0], [W, 0], [W, H], [0, H]]
  classes.forEach((o, j) => { if (j !== i) poly = clip(poly, cl.c, o.c) })
  return { color: cl.color, d: 'M' + poly.map(p => p.map(v => v.toFixed(1)).join(' ')).join('L') + 'Z' }
})
const showRegions = computed(() => props.mode === 'linear' || props.mode === 'finetune')
const wrong = (p: { ci: number; raw: number[]; ft: number[] }) => showRegions.value && nearest(pos(p)) !== p.ci
</script>

<template>
  <figure class="emb" :style="{ width: `${width}px` }">
    <svg :width="width" :viewBox="`0 0 ${W} ${H}`">
      <rect x="0" y="0" :width="W" :height="H" rx="8" fill="#fafaf8" stroke="var(--rule)" />
      <path v-for="(r, i) in regions" :key="i" :d="r.d" :fill="r.color" class="region"
        :style="{ fillOpacity: showRegions ? 0.14 : 0, strokeOpacity: showRegions ? 1 : 0 }" stroke="#fafaf8" stroke-width="2" />
      <circle
        :cx="query.raw[0]" :cy="query.raw[1]" :r="knn.r" fill="none" stroke="var(--ink)" stroke-width="1.6"
        pathLength="1" stroke-dasharray="1" :stroke-dashoffset="mode === 'knn' ? 0 : 1" class="ring"
        :class="{ on: mode === 'knn' }"
      />
      <g v-for="(p, i) in pts" :key="i" class="pt" :style="{ transform: `translate(${pos(p)[0]}px, ${pos(p)[1]}px)` }">
        <circle r="6" :fill="classes[p.ci].color" :opacity="mode === 'knn' && !knn.ids.has(i) ? 0.35 : 1" class="dot" />
        <circle r="10" fill="none" stroke="var(--ink)" stroke-width="1.8" class="fade"
          :style="{ opacity: (mode === 'knn' && knn.ids.has(i)) || wrong(p) ? 1 : 0 }" :stroke-dasharray="wrong(p) ? '3 2' : 'none'" />
      </g>
      <g class="pt" :style="{ transform: `translate(${pos(query)[0]}px, ${pos(query)[1]}px)` }">
        <circle r="8.5" fill="white" stroke="var(--ink)" stroke-width="3" />
        <text x="13" y="-9" class="q">new image</text>
      </g>
    </svg>
    <figcaption>
      <span v-for="cl in classes" :key="cl.name" class="key"><i :style="{ background: cl.color }" />{{ cl.name }}</span>
      <span class="muted">· sketch</span>
    </figcaption>
  </figure>
</template>

<style scoped>
.emb { margin: 0; }
svg { display: block; }
.pt { transition: transform 900ms cubic-bezier(.3,.7,.2,1); }
.dot { transition: opacity 400ms; }
.fade { transition: opacity 450ms; }
.region { transition: fill-opacity 450ms, stroke-opacity 450ms; }
.ring { opacity: 0; visibility: hidden; transition: stroke-dashoffset 700ms ease-out, opacity 300ms, visibility 0s 300ms; }
.ring.on { opacity: 1; visibility: visible; transition: stroke-dashoffset 700ms ease-out, opacity 300ms, visibility 0s; }
.q { font-size: 12px; font-weight: 700; fill: var(--ink); paint-order: stroke; stroke: #fafaf8; stroke-width: 4px; stroke-linejoin: round; }
figcaption { font-size: 12px; margin-top: 6px; }
.key { margin-right: 10px; }
.key i { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 4px; vertical-align: 0; }
</style>
