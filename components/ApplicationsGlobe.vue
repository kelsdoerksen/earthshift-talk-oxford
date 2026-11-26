<script setup lang="ts">
import { asset } from '../utils/asset'
// The research question slide: a turning dot-globe with five real-world applications around it, each shown with an
// EarthShift tile. Tiles arrive one after another, then a pulse runs from the globe to each application in turn and
// highlights it. Real-time loop; purely illustrative (no data).
import { onMounted, onUnmounted, ref } from 'vue'
import { drawGlobe, setupCanvas, type GlobeStyle } from '../utils/globe'

const W = 980, H = 552
const canvas = ref<HTMLCanvasElement>()
let raf = 0, t0 = -1
const FONT = '"Liberation Sans", Helvetica, Arial, sans-serif'
const G: GlobeStyle = { cx: 490, cy: 366, r: 92, spin: 0, tilt: 0.38 }
const T = 80
const APPS = [
  { name: 'Damage assessment', tile: 'bright_turkey_rgb_id', x: 145, y: 300, lab: 'below' },
  { name: 'Flood mapping', tile: 'sen1floods11_s2_id', x: 240, y: 462, lab: 'below' },
  { name: 'Crop mapping', tile: 'rpg_2017_id', x: 490, y: 506, lab: 'left' },
  { name: 'Cloud segmentation', tile: 'cloudsen12_l2a_id', x: 740, y: 462, lab: 'below' },
  { name: 'Image classification', tile: 'resisc45_harbor_id', x: 835, y: 300, lab: 'below' },
].map(a => ({ ...a, img: Object.assign(new Image(), { src: asset(`/tiles/clean/${a.tile}.png`) }) }))
const CYCLE = 1.6

function frame(ms: number) {
  raf = requestAnimationFrame(frame)
  const c = canvas.value
  if (!c || c.offsetParent === null) { t0 = -1; return }
  const g = c.getContext('2d')!, now = ms / 1000
  if (t0 < 0) t0 = now
  const t = now - t0
  g.clearRect(0, 0, W, H)
  G.spin = now * (2 * Math.PI / 60)

  const active = t > 2.6 ? Math.floor((t - 2.6) / CYCLE) % APPS.length : -1
  const u = t > 2.6 ? ((t - 2.6) % CYCLE) / CYCLE : 0

  APPS.forEach((a, i) => {
    const appear = Math.min(1, Math.max(0, (t - 0.3 - i * 0.4) / 0.5))
    if (appear <= 0) return
    // connector from the globe's rim to the tile
    const dx = a.x - G.cx, dy = a.y - G.cy, d = Math.hypot(dx, dy)
    const x0 = G.cx + (dx / d) * (G.r + 6), y0 = G.cy + (dy / d) * (G.r + 6)
    const x1 = a.x - (dx / d) * (T * 0.62), y1 = a.y - (dy / d) * (T * 0.62)
    g.globalAlpha = appear
    g.strokeStyle = i === active ? '#2b7bd8' : '#c7cfd9'; g.lineWidth = i === active ? 2.5 : 1.5
    g.setLineDash([4, 5]); g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke(); g.setLineDash([])
    if (i === active && u < 0.5) {
      const f = u / 0.5, px = x0 + (x1 - x0) * f, py = y0 + (y1 - y0) * f
      g.fillStyle = '#2b7bd8'; g.beginPath(); g.arc(px, py, 5, 0, Math.PI * 2); g.fill()
    }
    // tile
    const hl = i === active ? Math.sin(Math.min(1, Math.max(0, (u - 0.4) / 0.6)) * Math.PI) : 0
    const s = T * (0.85 + 0.15 * appear) * (1 + 0.1 * hl)
    g.fillStyle = hl > 0 ? '#2b7bd8' : '#ffffff'
    g.shadowColor = 'rgba(0,0,0,0.18)'; g.shadowBlur = 6
    g.fillRect(a.x - s / 2 - 4, a.y - s / 2 - 4, s + 8, s + 8); g.shadowBlur = 0
    if (a.img.complete && a.img.naturalWidth) g.drawImage(a.img, a.x - s / 2, a.y - s / 2, s, s)
    g.font = `700 16px ${FONT}`; g.fillStyle = hl > 0.2 ? '#2b7bd8' : '#1f2328'; g.textBaseline = 'middle'
    if (a.lab === 'below') { g.textAlign = 'center'; g.fillText(a.name, a.x, a.y + T / 2 + 18) }
    else if (a.lab === 'left') { g.textAlign = 'right'; g.fillText(a.name, a.x - T / 2 - 14, a.y) }
    else { g.textAlign = 'left'; g.fillText(a.name, a.x + T / 2 + 14, a.y) }
    g.globalAlpha = 1
  })
  drawGlobe(g, G)
}

onMounted(() => { if (canvas.value) setupCanvas(canvas.value, W, H); raf = requestAnimationFrame(frame) })
onUnmounted(() => cancelAnimationFrame(raf))
</script>

<template>
  <canvas ref="canvas" class="apps-globe" aria-label="A globe surrounded by five Earth observation applications" />
</template>

<style scoped>
.apps-globe { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; }
</style>
