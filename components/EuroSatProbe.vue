<script setup lang="ts">
// "Embeddings in action": a frozen GFM (DINOv2 ViT-S/14) turns EuroSAT images into 384 numbers; those land as dots on a
// 2-D map (t-SNE detail); a new image is labelled by k-NN, by a linear probe, or by fine-tuning.
// Port of slide 11 (beats 1-12) of H. Kerner's "State of GeoAI" deck (Taylor Geospatial, SatSummit 2026), drawn from the
// same data: data/eurosat_probe.json. The fine-tune beat's map, borders and numbers are MOCK (illustration only), as in
// the source deck. Laid out on a 1920 x 1080 stage scaled to the slide.
// step (= $clicks, slide `clicks: 11`): 0 known · 1 model · 2 embed · 3 plot · 4 more · 5 all · 6 labels · 7 image ·
// 8 dot · 9 knn · 10 linear · 11 finetune
import { computed, onUnmounted, ref, watch } from 'vue'
import D from '../data/eurosat_probe.json'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 99 })
const s = computed(() => Math.min(props.step, 11))

// ---------------- layout (stage px, as the source deck)
const TILE = { x: 120, y: 250, s: 220 }
const MODEL = { x: 428, w: 296, h: 176 }
const NUM = { x: 800, w: 190 }
const MAP = { x: 1056, y: 250, w: 744, h: 700, pad: 56, fade: 44 }
const SLOT = { x: 120, a: 586, b: 652, c: 764 }
const MID = TILE.y + TILE.s / 2
const COL: Record<string, string> = { River: '#7b9bd9', Highway: '#3b1e1c', Pasture: '#6aa84f' }
const KNOWN = D.knn.neighbours.slice(0, 3)            // the deck's known images = our image's 3 nearest
const img = (id: string) => `/eurosat/${id}.jpg`

// ---------------- the map: one scale for x and y, fitted to the coloured classes + our image
type P = { id: string; label: string; x: number; y: number }
const lab = D.labelled as P[]
const sel = lab.filter(p => COL[p.label]).concat([D.hero as P])
const ux0 = Math.min(...sel.map(p => p.x)), ux1 = Math.max(...sel.map(p => p.x))
const uy0 = Math.min(...sel.map(p => p.y)), uy1 = Math.max(...sel.map(p => p.y))
const K = Math.min((MAP.w - 2 * MAP.pad) / (ux1 - ux0), (MAP.h - 2 * MAP.pad) / (uy1 - uy0))
const OX = MAP.x + (MAP.w - K * (ux1 - ux0)) / 2 - K * ux0, OY = MAP.y + (MAP.h - K * (uy1 - uy0)) / 2 - K * uy0
const mp = (x: number, y: number): [number, number] => [OX + K * x, OY + K * y]
const clamp01 = (v: number) => Math.max(0, Math.min(1, v))
const edge = ([x, y]: [number, number]) => clamp01(Math.min(x - MAP.x, MAP.x + MAP.w - x, y - MAP.y, MAP.y + MAP.h - y) / MAP.fade)
const pos1 = lab.map(p => mp(p.x, p.y))
const pos2 = (D.mock_finetune_map as number[][]).map(p => mp(p[0], p[1]))
const hero1 = mp(D.hero.x, D.hero.y)
const hero2 = mp(D.mock_finetune_hero_map[0], D.mock_finetune_hero_map[1])
const START: [number, number] = [NUM.x + NUM.w / 2, MID]          // dots come out of the embedding column

// ---------------- linear borders (the deck's 2-D rule) as exact regions inside the panel
type B = { coef: number[][]; intercept: number[]; mean: number[]; scale: number[]; hero_region: string }
function borderLines(b: B) {
  return b.coef.map((c, j) => {
    const a = c[0] / (K * b.scale[0]), bb = c[1] / (K * b.scale[1])
    return [a, bb, b.intercept[j] - a * OX - bb * OY - (c[0] * b.mean[0]) / b.scale[0] - (c[1] * b.mean[1]) / b.scale[1]]
  })
}
function regions(lines: number[][]) {
  const [x0, y0, x1, y1] = [MAP.x, MAP.y, MAP.x + MAP.w, MAP.y + MAP.h]
  return lines.map((_, k) => {
    let poly = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]
    for (let j = 0; j < lines.length && poly.length; j++) {
      if (j === k) continue
      const a = lines[k][0] - lines[j][0], b = lines[k][1] - lines[j][1], d = lines[k][2] - lines[j][2]
      const f = (p: number[]) => a * p[0] + b * p[1] + d, next: number[][] = []
      poly.forEach((p, i) => {
        const q = poly[(i + 1) % poly.length], fp = f(p), fq = f(q)
        if (fp >= 0) next.push(p)
        if ((fp >= 0) !== (fq >= 0)) { const t = fp / (fp - fq); next.push([p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])]) }
      })
      poly = next
    }
    return poly.length > 2 ? 'M' + poly.map(p => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join('L') + 'Z' : ''
  })
}
const heroK = D.classes.indexOf(D.borders.hero_region)
const reg1 = regions(borderLines(D.borders as B)), reg2 = regions(borderLines(D.mock_finetune_borders as unknown as B))

// ---------------- class-name placement: next to each class's dots, clear of every dot
// "Our image" label: up-right of our image on the first map, up-left on the fine-tuned one
const OUR = { w: 170, h: 36, dx: 66, dy: -66 }
const ourBox = (h: [number, number], left: boolean) => (left
  ? [h[0] - OUR.dx - OUR.w, h[1] + OUR.dy - OUR.h / 2 - 4, h[0] - OUR.dx, h[1] + OUR.dy + OUR.h / 2]
  : [h[0] + OUR.dx, h[1] + OUR.dy - OUR.h / 2 - 4, h[0] + OUR.dx + OUR.w, h[1] + OUR.dy + OUR.h / 2])
function placeNames(pts: [number, number][], hero: [number, number], ourLeft: boolean) {
  const boxes: number[][] = [ourBox(hero, ourLeft)]
  const obst = pts.filter(p => edge(p) > 0.05).concat([hero])
  const boxGap = (a: number[], b: number[]) => Math.hypot(Math.max(b[0] - a[2], a[0] - b[2], 0), Math.max(b[1] - a[3], a[1] - b[3], 0))
  return Object.keys(COL).map((name) => {
    const own = pts.filter((_, i) => lab[i].label === name && edge(pts[i]) > 0.5)
    const cx = own.reduce((a, p) => a + p[0], 0) / own.length, cy = own.reduce((a, p) => a + p[1], 0) / own.length
    const w = name.length * 23, h = 44
    const cands: [number, number][] = []
    for (const r of [70, 110, 150, 200]) for (let a = 0; a < 16; a++) {
      const t = (a / 16) * Math.PI * 2
      cands.push([r * Math.cos(t) - w / 2 + (Math.cos(t) * w) / 2, r * Math.sin(t)])
    }
    let best = cands[0], bestScore = -Infinity
    for (const [dx, dy] of cands) {
      const b = [cx + dx, cy + dy - h / 2, cx + dx + w, cy + dy + h / 2]
      if (b[0] < MAP.x + 24 || b[2] > MAP.x + MAP.w - 24 || b[1] < MAP.y + 24 || b[3] > MAP.y + MAP.h - 60) continue
      const dDots = Math.min(...obst.map(([x, y]) => Math.hypot(Math.max(b[0] - x, 0, x - b[2]), Math.max(b[1] - y, 0, y - b[3]))))
      const dBox = Math.min(...boxes.map(o => boxGap(b, o)))
      const clear = Math.min(dDots - 18, dBox - 14)
      const score = (clear > 0 ? 1000 : clear * 10) - Math.hypot(dx + w / 2, dy)   // clear first, then as close as possible
      if (score > bestScore) { bestScore = score; best = [dx, dy] }
    }
    boxes.push([cx + best[0], cy + best[1] - h / 2, cx + best[0] + w, cy + best[1] + h / 2])
    return { name, x: cx + best[0], y: cy + best[1] }
  })
}

const names1 = placeNames(pos1, hero1, false), names2 = placeNames(pos2, hero2, true)

// ---------------- k-NN circle (in the 2-D view: reaches the 5 real nearest neighbours)
const nbIdx = D.knn.neighbours.map(n => n.i)
const knnR = Math.max(...nbIdx.map(i => Math.hypot(pos1[i][0] - hero1[0], pos1[i][1] - hero1[1]))) + 26
const vote = D.knn.votes[0]

// ---------------- beat 5 ("more"): two more known images go through, one after the other
const sub = ref(2)
let timers: ReturnType<typeof setTimeout>[] = []
watch(() => props.step, (now, old) => {
  timers.forEach(clearTimeout); timers = []
  if (now === 4 && old === 3) { sub.value = 0; timers.push(setTimeout(() => (sub.value = 1), 250), setTimeout(() => (sub.value = 2), 2000)) }
  else sub.value = 2
}, { immediate: true })
onUnmounted(() => timers.forEach(clearTimeout))
const knownAt = computed(() => (s.value < 4 ? 0 : s.value === 4 ? sub.value : -1))

// ---------------- what each beat shows
const tileId = computed(() => (s.value >= 7 ? D.hero.id : knownAt.value >= 0 ? KNOWN[knownAt.value].id : null))
const numbers = computed<number[] | null>(() => {
  if (s.value < 2 || s.value === 5 || s.value === 6) return null
  if (s.value >= 7) return s.value === 11 ? D.mock_finetune_numbers : D.embedding.first
  return (D.known_numbers as Record<string, number[]>)[KNOWN[Math.max(0, knownAt.value)].id]
})
const knownShown = (k: number) => (k === 0 ? s.value >= 3 : s.value > 4 || (s.value === 4 && sub.value >= k))
const dots = computed(() => lab.map((p, i) => {
  const kk = KNOWN.findIndex(n => n.i === i)
  const shown = kk >= 0 ? knownShown(kk) : s.value >= 5
  const at = shown ? (s.value === 11 ? pos2[i] : pos1[i]) : START
  const e = edge(s.value === 11 ? pos2[i] : pos1[i])
  const dim = s.value === 9 && !nbIdx.includes(i)
  return { i, at, fill: COL[p.label], op: shown ? e * (dim ? 0.3 : 1) : 0, ring: s.value === 9 && nbIdx.includes(i), delay: kk >= 0 ? (kk === 0 ? 0 : 350) : 200 + i * 9 }
}))
const heroAt = computed(() => (s.value >= 8 ? (s.value === 11 ? hero2 : hero1) : START))
const names = computed(() => (s.value === 11 ? names2 : names1))
const showNames = computed(() => s.value >= 6 && s.value !== 9)
const caption = computed(() => (s.value === 9 ? 'KNN-5: the 5 nearest vote' : s.value === 10 ? 'Linear: draw borders' : s.value === 11 ? 'Fine-tune: the model itself is updated' : ''))
const answer = computed(() => (s.value === 9 ? vote.label : s.value === 10 ? D.linear.answer : s.value === 11 ? D.hero.label : ''))
const fmt = (v: number) => (v < 0 ? '−' : '') + Math.abs(v).toFixed(2)
</script>

<template>
  <div class="es-wrap">
    <div class="es-stage">
      <!-- the pipeline strip -->
      <div class="tile fade" :class="{ on: !!tileId }" :style="{ left: TILE.x + 'px', top: TILE.y + 'px', width: TILE.s + 'px', height: TILE.s + 'px' }">
        <img v-for="id in [KNOWN[0].id, KNOWN[1].id, KNOWN[2].id, D.hero.id]" :key="id" :src="img(id)" class="px" :class="{ on: tileId === id }" :alt="id">
      </div>
      <div class="tlab fade" :class="{ on: !!tileId && s < 9 }" :style="{ left: TILE.x + 'px', top: TILE.y + TILE.s + 14 + 'px' }">
        <template v-if="s >= 7"><b>?</b><div>unknown label</div></template>
        <template v-else-if="knownAt >= 0"><b :style="{ color: COL[KNOWN[knownAt].label] }">{{ KNOWN[knownAt].label }}</b><div>known label</div></template>
      </div>

      <div class="arrow fade" :class="{ on: s >= 1 }" :style="{ left: TILE.x + TILE.s + 18 + 'px', top: MID - 2 + 'px', width: '48px' }" />
      <div class="model fade" :class="{ on: s >= 1, open: s === 11 }" :style="{ left: MODEL.x + 'px', top: MID - MODEL.h / 2 + 'px', width: MODEL.w + 'px', height: MODEL.h + 'px' }">
        <svg width="34" height="44" viewBox="0 0 34 44" class="lock">
          <path :d="s === 11 ? 'M9 20 V12 a8 8 0 0 1 16 0 V8' : 'M9 20 V12 a8 8 0 0 1 16 0 V20'" fill="none" stroke="currentColor" stroke-width="5" />
          <rect x="3" y="20" width="28" height="22" rx="4" fill="currentColor" />
        </svg>
        <b>{{ s === 11 ? 'Unfrozen model' : 'Frozen model' }}</b>
      </div>
      <div class="arrow fade" :class="{ on: s >= 2 }" :style="{ left: MODEL.x + MODEL.w + 18 + 'px', top: MID - 2 + 'px', width: '48px' }" />
      <div class="nums fade" :class="{ on: s >= 2 }" :style="{ left: NUM.x + 'px', top: TILE.y + 'px', width: NUM.w + 'px', height: TILE.s + 'px' }">
        <div v-for="(v, k) in (numbers || [0, 0, 0, 0, 0])" :key="k" class="n" :style="{ opacity: numbers ? 1 : 0 }">{{ fmt(v) }}</div>
        <div class="more">⋮</div>
      </div>
      <div class="numlab fade" :class="{ on: s >= 2 }" :style="{ left: NUM.x - 10 + 'px', top: TILE.y + TILE.s + 14 + 'px' }">
        <b>{{ D.embedding.dim }} numbers</b><div>embedding</div>
      </div>

      <!-- probe column -->
      <div class="probe fade" :class="{ on: s >= 9 }" :style="{ left: SLOT.x + 'px', top: '530px', width: '600px' }">Probe</div>
      <div class="cap" :style="{ left: SLOT.x + 'px', top: SLOT.a + 'px' }"><span class="fade" :class="{ on: !!caption }">{{ caption }}</span></div>
      <div class="ans" :style="{ left: SLOT.x + 'px', top: SLOT.b + 'px' }">
        <span class="fade" :class="{ on: !!answer }" :style="{ color: COL[answer] }">{{ answer }}</span>
        <span v-if="s === 9" class="votes">{{ vote.n }} / {{ D.knn.k }}</span>
      </div>
      <div class="nbrow fade" :class="{ on: s === 9 }" :style="{ left: SLOT.x + 'px', top: SLOT.c + 'px' }">
        <figure v-for="n in D.knn.neighbours" :key="n.id">
          <img :src="img(n.id)" class="px" :style="{ borderColor: COL[n.label] || '#999' }" :alt="n.label">
          <figcaption>{{ n.label }}</figcaption>
        </figure>
      </div>
      <div class="mock fade" :class="{ on: s === 11 }" :style="{ left: SLOT.x + 'px', top: '880px' }">Illustration: no fine-tune was run for this example</div>

      <!-- the map panel -->
      <div class="panel fade" :class="{ on: s >= 3 }" :style="{ left: MAP.x + 'px', top: MAP.y + 'px', width: MAP.w + 'px', height: MAP.h + 'px' }" />
      <div class="mapcap fade" :class="{ on: s >= 5 }" :style="{ left: MAP.x + MAP.w + 'px', top: MAP.y - 46 + 'px' }">{{ D.labelled.length }} of the EuroSAT training images</div>
      <svg class="map" width="1920" height="1080" viewBox="0 0 1920 1080">
        <defs><clipPath id="es-clip"><rect :x="MAP.x + 3" :y="MAP.y + 3" :width="MAP.w - 6" :height="MAP.h - 6" rx="6" /></clipPath></defs>
        <g clip-path="url(#es-clip)">
          <g class="fade" :class="{ on: s === 10 }">
            <path :d="reg1[heroK]" class="tint" />
            <path v-for="(d, k) in reg1" :key="'r1' + k" :d="d" class="border" />
          </g>
          <g class="fade" :class="{ on: s === 11 }">
            <path :d="reg2[heroK]" class="tint" />
            <path v-for="(d, k) in reg2" :key="'r2' + k" :d="d" class="border" />
          </g>
          <circle :cx="hero1[0]" :cy="hero1[1]" :r="knnR" class="knn" :class="{ on: s === 9 }" />
          <g v-for="d in dots" :key="d.i" class="dot" :style="{ transform: `translate(${d.at[0]}px, ${d.at[1]}px)`, opacity: d.op, transitionDelay: `${d.delay}ms` }">
            <circle r="12" :class="d.fill ? 'c' : 'c other'" :style="d.fill ? { fill: d.fill } : {}" />
            <circle r="20" class="ring" :style="{ opacity: d.ring ? 1 : 0 }" />
          </g>
          <g class="dot" :style="{ transform: `translate(${heroAt[0]}px, ${heroAt[1]}px)`, opacity: s >= 8 ? 1 : 0 }">
            <circle r="16" class="hero" /><circle r="5" class="hero-c" />
          </g>
        </g>
        <g class="fade" :class="{ on: s === 8 || s === 11 }">
          <line :x1="heroAt[0] + (s === 11 ? -14 : 14)" :y1="heroAt[1] - 14" :x2="heroAt[0] + (s === 11 ? -60 : 60)" :y2="heroAt[1] - 60" class="lead" />
          <text :x="heroAt[0] + (s === 11 ? -66 : 66)" :y="heroAt[1] - 58" :text-anchor="s === 11 ? 'end' : 'start'" class="ourimg">Our image</text>
        </g>
        <g v-for="n in names" :key="n.name" class="name" :style="{ transform: `translate(${n.x}px, ${n.y}px)`, opacity: showNames ? 1 : 0 }">
          <text :fill="COL[n.name]" dominant-baseline="middle">{{ n.name }}</text>
        </g>
        <g class="fade" :class="{ on: showNames && s !== 11 }">
          <circle :cx="MAP.x + 30" :cy="MAP.y + MAP.h - 28" r="10" class="c other" />
          <text :x="MAP.x + 50" :y="MAP.y + MAP.h - 28" dominant-baseline="middle" class="otherlab">Other classes</text>
        </g>
      </svg>
    </div>
  </div>
</template>

<style scoped>
.es-wrap { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
.es-stage { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform: scale(calc(980 / 1920)); transform-origin: 0 0; color: #3b1e1c; font-family: "Liberation Sans", Helvetica, Arial, sans-serif; }
.es-stage > * { position: absolute; }
.fade { opacity: 0; transition: opacity 500ms ease; }
.fade.on { opacity: 1; }
.px { image-rendering: pixelated; }
.tile { border-radius: 6px; overflow: hidden; }
.tile img { position: absolute; left: 0; top: 0; width: 220px; height: 220px; max-width: none; object-fit: cover; opacity: 0; transition: opacity 400ms; }
.tile img.on { opacity: 1; }
.tlab b, .numlab b { font-size: 34px; }
.tlab div, .numlab div { font-size: 32px; margin-top: 4px; }
.arrow { height: 4px; background: #3b1e1c; }
.arrow::after { content: ""; position: absolute; right: -14px; top: -9px; border-left: 16px solid #3b1e1c; border-top: 11px solid transparent; border-bottom: 11px solid transparent; }
.model { border-radius: 12px; background: #3b1e1c; color: #f4f1ea; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; font-size: 34px; transition: opacity 500ms, background 600ms; }
.model.open { background: #7a625b; }
.lock path { transition: d 500ms; }
.nums { border-left: 4px solid #3b1e1c; border-right: 4px solid #3b1e1c; border-radius: 12px; display: flex; flex-direction: column; align-items: flex-end; justify-content: center; padding: 0 30px; font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 30px; line-height: 1.12; }
.nums .n { transition: opacity 300ms; }
.nums .more { align-self: center; color: #9a8f88; font-size: 24px; line-height: 1; }
.probe { font-size: 30px; color: #9a8f88; border-bottom: 2px solid #ddd6c8; padding-bottom: 6px; }
.cap { font-size: 40px; font-weight: 700; white-space: nowrap; }
.ans { font-size: 72px; font-weight: 700; white-space: nowrap; }
.votes { font-size: 34px; color: #6b5d58; margin-left: 14px; font-weight: 500; }
.nbrow { display: flex; gap: 20px; }
.nbrow figure { margin: 0; text-align: center; }
.nbrow img { width: 96px; height: 96px; border: 4px solid; border-radius: 4px; display: block; }
.nbrow figcaption { font-size: 26px; margin-top: 6px; }
.mock { font-size: 26px; color: #9a8f88; font-style: italic; }
.panel { background: #fbfaf6; border: 3px solid #ddd6c8; border-radius: 8px; }
.mapcap { font-size: 30px; color: #8a7d76; transform: translateX(-100%); white-space: nowrap; }
.map { left: 0; top: 0; overflow: visible; }
.dot { transition: transform 900ms cubic-bezier(.3,.7,.2,1), opacity 600ms; }
.c { stroke: #fbfaf6; stroke-width: 2.5; }
.c.other { fill: #ddd6c8; stroke: #a99d95; stroke-width: 1.5; }
.ring { fill: none; stroke: #3b1e1c; stroke-width: 3.5; transition: opacity 400ms; }
.hero { fill: #fbfaf6; stroke: #3b1e1c; stroke-width: 5; }
.hero-c { fill: #3b1e1c; }
.knn { fill: rgba(123,155,217,0.12); stroke: #3b1e1c; stroke-width: 3; opacity: 0; transition: opacity 500ms; }
.knn.on { opacity: 1; }
.border { fill: none; stroke: #8a7d76; stroke-width: 2.5; }
.tint { fill: rgba(123,155,217,0.22); stroke: none; }
.lead { stroke: #3b1e1c; stroke-width: 2.5; }
.ourimg { font-size: 30px; font-weight: 700; fill: #3b1e1c; paint-order: stroke; stroke: #fbfaf6; stroke-width: 6px; }
.name { transition: transform 900ms cubic-bezier(.3,.7,.2,1), opacity 500ms; }
.name text { font-size: 38px; font-weight: 700; paint-order: stroke; stroke: #fbfaf6; stroke-width: 7px; }
.otherlab { font-size: 26px; fill: #8a7d76; }
</style>
