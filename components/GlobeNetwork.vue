<script setup lang="ts">
// Part 2 opener: satellites circle a turning dot-globe, imaging the land under them (it lights up, then fades).
// Each image flies into a neural network, a pulse runs through it, and lights up an application on the right.
// Real-time loop (keeps moving while the slide rests). Orbits and timings are schematic, not real satellites.
// Inspired by the title slide of H. Kerner's SatSummit 2026 "State of GeoAI" deck; land data: Natural Earth.
import { onMounted, onUnmounted, ref } from 'vue'
import { drawGlobe, setupCanvas, view, LAND, type Vec3, type GlobeStyle } from '../utils/globe'

const props = withDefaults(defineProps<{ apps?: string[] }>(), {
  apps: () => ['Agriculture', 'Land cover', 'Disaster response', 'Climate risk'],
})

const W = 980, H = 552
const canvas = ref<HTMLCanvasElement>()
let raf = 0

const BLUE = '#2b7bd8', INK = '#1f2328', EDGE = '#d5dae1'
const TILES = ['ftw_germany_image_id', 'rpg_2017_id', 'sen1floods11_s2_id', 'chesapeake_naip_ood', 'ftw_cambodia_image_ood', 'cloudsen12_l2a_id', 'rpg_2022_ood']
  .map((n) => { const im = new Image(); im.src = `/tiles/clean/${n}.png`; return im })

const G: GlobeStyle = { cx: 225, cy: 336, r: 150, spin: 0, tilt: 0.32 }
const ORB = 1.3
// orbit planes in view space: inclination about x, rotated about y
const SATS = [
  { inc: 1.25, rot: 0.3, per: 13, ph: 0.0 },
  { inc: 0.6, rot: 2.1, per: 17, ph: 2.2 },
  { inc: -0.35, rot: 4.0, per: 21, ph: 4.1 },
].map((s) => {
  const A: Vec3 = [Math.cos(s.rot), 0, Math.sin(s.rot)]
  const B: Vec3 = [-Math.sin(s.rot) * Math.cos(s.inc), Math.sin(s.inc), Math.cos(s.rot) * Math.cos(s.inc)]
  return { A, B, w: (2 * Math.PI) / s.per, ph: s.ph, next: 1 + s.ph / 2 }
})
const satPos = (s: typeof SATS[number], t: number): Vec3 => {
  const a = s.ph + s.w * t, c = Math.cos(a), n = Math.sin(a)
  return [c * s.A[0] + n * s.B[0], c * s.A[1] + n * s.B[1], c * s.A[2] + n * s.B[2]]
}

// network
const LX = [505, 595, 685, 775], LN = [4, 6, 6, 4]
const nodes = LX.map((x, l) => Array.from({ length: LN[l] }, (_, i) => ({ x, y: G.cy + (i - (LN[l] - 1) / 2) * (l === 0 || l === 3 ? 62 : 50) })))
const APP_X = 806

interface Packet { t0: number; x0: number; y0: number; to: number; img: HTMLImageElement }
interface Pulse { t0: number; path: number[] }
const packets: Packet[] = []
const pulses: Pulse[] = []
const appFlash = props.apps.map(() => -99)
const nodeFlash = nodes.map(l => l.map(() => -99))
const seen = new Float32Array(LAND.length).fill(-99)
let nextInput = 0, nextTile = 0
const STEP = 0.28 // seconds per layer

function frame(ms: number) {
  raf = requestAnimationFrame(frame)
  const c = canvas.value
  if (!c || c.offsetParent === null) return
  const g = c.getContext('2d')!
  const t = ms / 1000
  g.clearRect(0, 0, W, H)
  G.spin = t * (2 * Math.PI / 70)

  // satellites: positions, swaths, emissions
  const sp = SATS.map(s => satPos(s, t))
  for (let i = 0; i < LAND.length; i++) {
    const v = view(LAND[i], G.spin, G.tilt)
    if (v[2] <= 0) continue
    for (const p of sp) if (v[0] * p[0] + v[1] * p[1] + v[2] * p[2] > 0.985) seen[i] = t
  }
  SATS.forEach((s, k) => {
    const p = sp[k]
    if (t > s.next) {
      s.next = t + 2.4 + k * 0.4
      if (p[2] > 0.15) {
        const sx = G.cx + G.r * ORB * p[0], sy = G.cy - G.r * ORB * p[1]
        packets.push({ t0: t, x0: sx, y0: sy, to: nextInput, img: TILES[nextTile] })
        nextInput = (nextInput + 1) % LN[0]; nextTile = (nextTile + 1) % TILES.length
      }
    }
  })

  // orbits behind the globe
  const orbit = (front: boolean) => SATS.forEach((s) => {
    g.beginPath()
    let pen = false
    for (let k = 0; k <= 120; k++) {
      const a = (k / 120) * Math.PI * 2, c2 = Math.cos(a), n2 = Math.sin(a)
      const p: Vec3 = [c2 * s.A[0] + n2 * s.B[0], c2 * s.A[1] + n2 * s.B[1], c2 * s.A[2] + n2 * s.B[2]]
      const x = G.cx + G.r * ORB * p[0], y = G.cy - G.r * ORB * p[1]
      const draw = (p[2] >= 0) === front
      if (draw && pen) g.lineTo(x, y); else g.moveTo(x, y)
      pen = draw
    }
    g.setLineDash([3, 5]); g.strokeStyle = front ? '#9aa4b2' : '#d3d8df'; g.lineWidth = 1.2; g.stroke(); g.setLineDash([])
  })
  orbit(false)
  const drawSat = (p: Vec3) => {
    const x = G.cx + G.r * ORB * p[0], y = G.cy - G.r * ORB * p[1]
    g.fillStyle = BLUE; g.fillRect(x - 13, y - 3, 8, 6); g.fillRect(x + 5, y - 3, 8, 6)
    g.fillStyle = INK; g.fillRect(x - 4, y - 4, 8, 8)
  }
  sp.forEach(p => { if (p[2] < 0 && Math.hypot(p[0], p[1]) * ORB > 1) drawSat(p) })

  drawGlobe(g, G, (_v, i) => {
    const age = t - seen[i]
    return age < 5 ? `rgba(43,123,216,${(1 - age / 5).toFixed(3)})` : null
  })
  orbit(true)
  sp.forEach(p => { if (p[2] >= 0) drawSat(p) })

  // network edges
  g.lineWidth = 1; g.strokeStyle = EDGE
  for (let l = 0; l < 3; l++) for (const a of nodes[l]) for (const b of nodes[l + 1]) { g.beginPath(); g.moveTo(a.x, a.y); g.lineTo(b.x, b.y); g.stroke() }

  // pulses: one lit edge per layer, then the node, then the app
  for (let k = pulses.length - 1; k >= 0; k--) {
    const P = pulses[k], e = (t - P.t0) / STEP
    if (e > 4.5) { pulses.splice(k, 1); continue }
    for (let l = 0; l < 3; l++) {
      const f = Math.min(1, Math.max(0, e - l))
      if (f <= 0) continue
      const a = nodes[l][P.path[l]], b = nodes[l + 1][P.path[l + 1]]
      const fade = Math.max(0, 1 - Math.max(0, e - l - 1) / 1.5)
      g.strokeStyle = `rgba(43,123,216,${fade.toFixed(3)})`; g.lineWidth = 3
      g.beginPath(); g.moveTo(a.x, a.y); g.lineTo(a.x + (b.x - a.x) * f, a.y + (b.y - a.y) * f); g.stroke()
      if (f >= 1 && nodeFlash[l + 1][P.path[l + 1]] < P.t0 + (l + 1) * STEP) nodeFlash[l + 1][P.path[l + 1]] = t
    }
    if (e >= 3 && appFlash[P.path[3]] < P.t0 + 3 * STEP) appFlash[P.path[3]] = t
  }

  // nodes
  nodes.forEach((layer, l) => layer.forEach((n, i) => {
    const glow = Math.max(0, 1 - (t - nodeFlash[l][i]) / 0.8)
    g.beginPath(); g.arc(n.x, n.y, 10, 0, Math.PI * 2)
    g.fillStyle = glow > 0 ? `rgba(43,123,216,${(0.25 + 0.75 * glow).toFixed(3)})` : '#ffffff'; g.fill()
    g.lineWidth = 3.5; g.strokeStyle = INK; g.stroke()
  }))

  // applications
  props.apps.forEach((name, i) => {
    const y = nodes[3][i].y, glow = Math.max(0, 1 - (t - appFlash[i]) / 1.4)
    g.strokeStyle = glow > 0 ? `rgba(43,123,216,${(0.3 + 0.7 * glow).toFixed(3)})` : EDGE; g.lineWidth = glow > 0 ? 2.5 : 1
    g.beginPath(); g.moveTo(nodes[3][i].x + 12, y); g.lineTo(APP_X - 6, y); g.stroke()
    g.font = `${glow > 0 ? 700 : 500} 16px "Liberation Sans", Helvetica, Arial, sans-serif`
    g.fillStyle = glow > 0 ? BLUE : INK; g.textBaseline = 'middle'
    g.fillText(name, APP_X, y)
  })

  // image packets flying from a satellite to an input neuron
  for (let k = packets.length - 1; k >= 0; k--) {
    const P = packets[k], u = (t - P.t0) / 1.2
    const tgt = nodes[0][P.to]
    if (u >= 1) {
      packets.splice(k, 1)
      nodeFlash[0][P.to] = t
      pulses.push({ t0: t, path: [P.to, Math.floor(Math.random() * LN[1]), Math.floor(Math.random() * LN[2]), Math.floor(Math.random() * LN[3])] })
      continue
    }
    const e = u < 0.5 ? 2 * u * u : 1 - (-2 * u + 2) ** 2 / 2
    const cx = (P.x0 + tgt.x) / 2, cy = Math.min(P.y0, tgt.y) - 90
    const x = (1 - e) ** 2 * P.x0 + 2 * (1 - e) * e * cx + e * e * tgt.x
    const y = (1 - e) ** 2 * P.y0 + 2 * (1 - e) * e * cy + e * e * tgt.y
    const s = 30 - 14 * e
    g.fillStyle = '#fff'; g.fillRect(x - s / 2 - 2, y - s / 2 - 2, s + 4, s + 4)
    if (P.img.complete && P.img.naturalWidth) g.drawImage(P.img, x - s / 2, y - s / 2, s, s)
  }
}

onMounted(() => { if (canvas.value) setupCanvas(canvas.value, W, H); raf = requestAnimationFrame(frame) })
onUnmounted(() => cancelAnimationFrame(raf))
</script>

<template>
  <canvas ref="canvas" class="globe-net" aria-label="Satellites image the Earth; the images feed a neural network that serves applications" />
</template>

<style scoped>
.globe-net { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; }
</style>
