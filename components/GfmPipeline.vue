<script setup lang="ts">
// What a geospatial foundation model is, and the ways to use one (after Kelsey's TreeSense talk, slides 4-6).
// phase: 0 pretraining tiles · 1 + network · 2 + embedding box
// head:  'none' · 'knn' (frozen, no training: vote of labelled neighbours)
//        'linear' (frozen backbone, only the last layer trained) · 'finetune' (every layer trained)
// Illustration only: no data. Tiles are EarthShift tiles, badge-free crops in public/tiles/clean.
import { computed } from 'vue'

type Head = 'none' | 'knn' | 'linear' | 'finetune'
const props = withDefaults(defineProps<{ phase?: number; head?: Head; width?: number }>(),
  { phase: 99, head: 'none', width: 620 })

const tiles = [
  { src: 'ftw_germany_image_id', x: 8, y: 22 },
  { src: 'chesapeake_naip_ood', x: 60, y: 50 },
  { src: 'sen1floods11_s2_id', x: 12, y: 122 },
  { src: 'rpg_2017_id', x: 64, y: 150 },
]
const L = [
  { x: 236, ys: [100, 155, 210] },
  { x: 296, ys: [78, 128, 178, 228] },
  { x: 360, ys: [125, 185] },
]
const edges = computed(() => {
  const out: { x1: number; y1: number; x2: number; y2: number }[] = []
  for (let l = 0; l < L.length - 1; l++)
    for (const y1 of L[l].ys) for (const y2 of L[l + 1].ys) out.push({ x1: L[l].x, y1, x2: L[l + 1].x, y2 })
  return out
})
const outs = [{ y: 100, label: 'maize' }, { y: 155, label: 'wheat' }, { y: 210, label: 'peas' }]
const headEdges = computed(() => L[2].ys.flatMap(y1 => outs.map(o => ({ x1: L[2].x, y1, x2: 462, y2: o.y }))))

const FROZEN = '#8fa3b8'
const TRAIN = 'var(--accent)'
const netColor = computed(() => props.head === 'finetune' ? TRAIN : (props.head === 'none' ? 'var(--ink)' : FROZEN))
const showHead = computed(() => props.head !== 'none')
const headTrained = computed(() => props.head === 'linear' || props.head === 'finetune')
</script>

<template>
  <svg :width="width" :viewBox="`0 0 640 300`" class="pipe">
    <!-- pretraining data -->
    <g class="fade" :style="{ opacity: phase >= 0 ? 1 : 0 }">
      <g v-for="t in tiles" :key="t.src">
        <rect :x="t.x - 2" :y="t.y - 2" width="92" height="92" fill="white" />
        <image :href="`/tiles/clean/${t.src}.png`" :x="t.x" :y="t.y" width="88" height="88" preserveAspectRatio="xMidYMid slice" />
      </g>
      <text x="80" y="268" text-anchor="middle" class="lbl b">Large unlabeled</text>
      <text x="80" y="286" text-anchor="middle" class="lbl">pretraining data</text>
    </g>

    <!-- arrow + network -->
    <g class="fade" :style="{ opacity: phase >= 1 ? 1 : 0 }">
      <path d="M170 155 H206" class="arrow" />
      <path d="M200 148 L210 155 L200 162 Z" fill="var(--ink)" />
      <line v-for="(e, i) in edges" :key="i" v-bind="e" :stroke="netColor" stroke-width="3.5" class="col" />
      <template v-for="(l, li) in L" :key="li">
        <circle v-for="y in l.ys" :key="y" :cx="l.x" :cy="y" r="12" fill="white" :stroke="netColor" stroke-width="7" class="col" />
      </template>
      <text x="296" y="22" text-anchor="middle" class="lbl b" :style="{ opacity: head === 'none' ? 1 : 0 }">Foundation model</text>
      <!-- frozen / fine-tuned badges -->
      <g class="fade" :style="{ opacity: head === 'knn' || head === 'linear' ? 1 : 0 }">
        <text x="214" y="22" class="lbl b" fill="#5d7084">❄ Frozen: weights fixed</text>
      </g>
      <g class="fade" :style="{ opacity: head === 'finetune' ? 1 : 0 }">
        <text x="214" y="22" class="lbl b" fill="var(--accent)">🔥 Fine-tuned: every layer updates</text>
      </g>
    </g>

    <!-- embedding -->
    <g class="fade" :style="{ opacity: phase >= 2 ? 1 : 0 }">
      <rect x="338" y="96" width="44" height="118" rx="4" fill="none" stroke="var(--gfm)" stroke-width="4" />
      <text x="360" y="240" text-anchor="middle" class="lbl b">Embedding</text>
      <text x="360" y="258" text-anchor="middle" class="lbl">(feature vector)</text>
    </g>

    <!-- task head -->
    <g class="fade" :style="{ opacity: showHead && phase >= 2 ? 1 : 0 }">
      <line
        v-for="(e, i) in headEdges" :key="i" v-bind="e" pathLength="1" class="draw"
        :stroke="headTrained ? TRAIN : '#9ca3af'" :stroke-width="headTrained ? 2.5 : 1.6"
        :stroke-dasharray="headTrained ? '1 0' : '0.04 0.04'"
      />
      <g v-for="o in outs" :key="o.label">
        <circle cx="478" :cy="o.y" r="16" fill="#f4f1ea" :stroke="headTrained ? TRAIN : '#9ca3af'" stroke-width="2.5" class="col" />
        <text x="502" :y="o.y + 5" class="lbl">{{ o.label }}</text>
      </g>
      <text x="478" y="52" text-anchor="middle" class="lbl b" :fill="headTrained ? 'var(--accent)' : 'var(--muted)'">
        {{ head === 'knn' ? 'No training' : 'Trained with labels' }}
      </text>
      <text x="478" y="70" text-anchor="middle" class="lbl small">
        {{ head === 'knn' ? 'vote of nearest labelled examples' : head === 'linear' ? 'only this last layer learns' : 'head + backbone learn together' }}
      </text>
    </g>
  </svg>
</template>

<style scoped>
.pipe { display: block; overflow: visible; }
.lbl { font-size: 15px; fill: var(--ink); }
.lbl.b { font-weight: 700; }
.lbl.small { font-size: 13px; fill: var(--muted); }
.arrow { stroke: var(--ink); stroke-width: 4; fill: none; }
.fade { transition: opacity 500ms ease; }
.col { transition: stroke 600ms ease; }
.draw { transition: stroke 600ms ease; }
text { transition: fill 400ms; }
</style>
