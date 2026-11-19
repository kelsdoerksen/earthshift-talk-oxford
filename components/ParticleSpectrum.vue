<script setup lang="ts">
// "What is the particle?" (after Kelsey's lab-meeting deck "Are pixels and patches the right particles?", slide 2).
// Five answers to "what becomes one token", one per click (step >= i + 1). The purple cell is one particle.
// Illustration only: the land-cover grid is a fixed pattern, not data.
const props = withDefaults(defineProps<{ step?: number; size?: number }>(), { step: 99, size: 132 })

const P = '#7b3fa0'                       // the particle (not ID/OOD colours)
const G = ['#93b071', '#b3c993', '#6f8c4f', '#c8b68a', '#a7bf86']
// fixed 8x8 land-cover pattern
const pat = [
  0, 1, 0, 2, 1, 0, 2, 1, 2, 1, 1, 0, 2, 0, 3, 2, 0, 2, 1, 1, 0, 2, 0, 1, 1, 0, 2, 0, 1, 1, 3, 2,
  2, 1, 0, 1, 4, 0, 1, 2, 4, 3, 4, 3, 1, 3, 4, 2, 2, 0, 3, 1, 2, 0, 1, 3, 0, 1, 1, 0, 2, 2, 1, 3,
]
const N = 8, C = 100 / N
const cells = pat.map((v, i) => ({ x: (i % N) * C, y: Math.floor(i / N) * C, fill: G[v] }))
// quadtree split: big blocks where the pattern is calm, small ones where it is busy
const quad = [
  { x: 0, y: 0, s: 50, f: G[0] }, { x: 50, y: 0, s: 25, f: G[3] }, { x: 75, y: 0, s: 25, f: G[2] },
  { x: 50, y: 25, s: 25, f: G[1] }, { x: 75, y: 25, s: 25, f: G[3] },
  { x: 0, y: 50, s: 25, f: G[2] }, { x: 25, y: 50, s: 12.5, f: G[1] }, { x: 37.5, y: 50, s: 12.5, f: G[3] },
  { x: 25, y: 62.5, s: 12.5, f: G[2] }, { x: 37.5, y: 62.5, s: 12.5, f: 'P' }, { x: 50, y: 50, s: 50, f: G[1] },
  { x: 0, y: 75, s: 25, f: G[0] }, { x: 25, y: 75, s: 25, f: G[2] },
]
const items = [
  { name: 'Pixel', what: 'one value per location' },
  { name: 'Patch', what: 'fixed block, e.g. 16×16 (ViT)' },
  { name: 'Adaptive', what: 'size or shape follows content' },
  { name: 'Scalar', what: 'one band at one pixel' },
  { name: 'Coordinate', what: 'query a continuous field' },
]
</script>

<template>
  <div class="row">
    <div v-for="(it, i) in items" :key="it.name" class="col" :class="{ on: step >= i + 1 }">
      <svg :width="size" :height="size" viewBox="-4 -4 108 108">
        <!-- pixel -->
        <g v-if="i === 0">
          <rect v-for="(c, k) in cells" :key="k" :x="c.x" :y="c.y" :width="C" :height="C" :fill="k === 21 ? P : c.fill" stroke="white" stroke-width="0.8" />
        </g>
        <!-- patch -->
        <g v-else-if="i === 1">
          <rect v-for="(c, k) in cells" :key="k" :x="c.x" :y="c.y" :width="C" :height="C" :fill="c.fill" stroke="white" stroke-width="0.8" />
          <path d="M0 0H100V100H0Z M50 0V100 M0 50H100" fill="none" stroke="var(--ink)" stroke-width="1.6" />
          <rect x="50" y="0" width="50" height="50" fill="none" :stroke="P" stroke-width="4" />
        </g>
        <!-- adaptive -->
        <g v-else-if="i === 2">
          <rect v-for="(q, k) in quad" :key="k" :x="q.x" :y="q.y" :width="q.s" :height="q.s" :fill="q.f === 'P' ? P : q.f" stroke="white" stroke-width="1.2" />
        </g>
        <!-- scalar: band stack -->
        <g v-else-if="i === 3">
          <g v-for="b in [2, 1, 0]" :key="b" :transform="`translate(${b * 14} ${-b * 12 + 24})`">
            <rect v-for="k in 16" :key="k" :x="((k - 1) % 4) * 17" :y="Math.floor((k - 1) / 4) * 17" width="17" height="17"
              :fill="b === 0 && k === 6 ? P : [G[3], G[1], G[2]][b]" stroke="white" stroke-width="0.9" />
          </g>
        </g>
        <!-- coordinate: continuous field -->
        <g v-else>
          <rect x="0" y="0" width="100" height="100" fill="#e6eeec" />
          <ellipse v-for="r in [14, 28, 42]" :key="r" cx="46" cy="56" :rx="r" :ry="r * 0.72" fill="none" stroke="#3f6f6a" stroke-width="1.4" />
          <circle cx="78" cy="30" r="6" :fill="P" />
          <text x="54" y="16" style="font-size: 11px" fill="var(--ink)">(x, y, t)</text>
        </g>
      </svg>
      <div class="name">{{ it.name }}</div>
      <div class="what muted">{{ it.what }}</div>
    </div>
  </div>
</template>

<style scoped>
.row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: 14px; }
.col { text-align: center; opacity: 0; transform: translateY(12px); transition: opacity 450ms, transform 450ms cubic-bezier(.2,.7,.2,1); }
.col.on { opacity: 1; transform: none; }
svg { display: block; margin: 0 auto; }
.name { font-weight: 700; font-size: 17px; margin-top: 8px; }
.what { font-size: 12.5px; line-height: 1.3; margin-top: 2px; }
</style>
