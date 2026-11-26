<script setup lang="ts">
import { asset } from '../utils/asset'
// Hook slide: the two BRIGHT earthquakes used in EarthShift's geographic shift.
// ID = Kahramanmaraş (Turkey–Syria) earthquake, OOD = Al Haouz (Morocco) earthquake (EarthShift paper, task list).
// step 0: the ID site · step >= arcAt: an arc flies to the OOD site, which lights up.
// Each site carries a small pre-event RGB sample from BRIGHT (public/tiles/clean). Real-time loop (the globe rocks gently).
import { onMounted, onUnmounted, ref } from 'vue'
import { drawGlobe, lonLat, project, setupCanvas, type GlobeStyle, type Vec3 } from '../utils/globe'

const props = withDefaults(defineProps<{ step?: number; arcAt?: number; width?: number; height?: number }>(), { step: 99, arcAt: 1, width: 560, height: 420 })
const canvas = ref<HTMLCanvasElement>()
let raf = 0, arcT0 = -1, lastOn = false
const ID = '#0072B2', OOD = '#D55E00'
const FONT = '"Liberation Sans", Helvetica, Arial, sans-serif'
const SITES = {
  id: { v: lonLat(36.94, 37.58), name: 'Kahramanmaraş, Türkiye–Syria', tag: 'Train (ID)', tile: 'bright_turkey_rgb_id' },
  ood: { v: lonLat(-8.39, 31.06), name: 'Al Haouz, Morocco', tag: 'Deploy (OOD)', tile: 'bright_morocco_rgb_ood' },
}
const img = (n: string) => { const i = new Image(); i.src = asset(`/tiles/clean/${n}.png`); return i }
const IMG = { id: img(SITES.id.tile), ood: img(SITES.ood.tile) }

function label(g: CanvasRenderingContext2D, lines: [string, string, number][], x: number, y: number, align: CanvasTextAlign) {
  g.textAlign = align; g.textBaseline = 'middle'; g.lineJoin = 'round'
  lines.forEach(([text, color, size], i) => {
    g.font = `${i === 0 ? 700 : 500} ${size}px ${FONT}`
    g.lineWidth = 5; g.strokeStyle = 'rgba(255,255,255,0.95)'; g.strokeText(text, x, y + i * (size + 5))
    g.fillStyle = color; g.fillText(text, x, y + i * (size + 5))
  })
}

function site(g: CanvasRenderingContext2D, G: GlobeStyle, key: 'id' | 'ood', color: string, t: number, alpha: number, side: 1 | -1) {
  const S = SITES[key], p = project(S.v, G)
  if (p.z <= 0 || alpha <= 0) return
  g.globalAlpha = alpha
  // a ring that grows from the site, fading in and out smoothly so it never pops back (no blink)
  const pulse = ((t + (key === 'ood' ? 0.9 : 0)) / 1.8) % 1
  g.strokeStyle = color; g.lineWidth = 2
  g.globalAlpha = alpha * Math.sin(Math.PI * pulse) * 0.9
  g.beginPath(); g.arc(p.x, p.y, 8 + 20 * pulse, 0, Math.PI * 2); g.stroke()
  g.globalAlpha = alpha
  g.fillStyle = color; g.beginPath(); g.arc(p.x, p.y, 6.5, 0, Math.PI * 2); g.fill()
  g.strokeStyle = 'white'; g.lineWidth = 2; g.stroke()
  // inset tile + label
  const T = 70, tx = side > 0 ? p.x + 22 : p.x - 22 - T, ty = p.y + 16
  g.fillStyle = color; g.fillRect(tx - 3, ty - 3, T + 6, T + 6)
  if (IMG[key].complete && IMG[key].naturalWidth) g.drawImage(IMG[key], tx, ty, T, T)
  label(g, [[S.tag, color, 15], [S.name, '#1f2328', 13]], side > 0 ? p.x + 20 : p.x - 20, p.y - 26, side > 0 ? 'left' : 'right')
  g.globalAlpha = 1
}

function frame(ms: number) {
  raf = requestAnimationFrame(frame)
  const c = canvas.value
  if (!c || c.offsetParent === null) return
  const g = c.getContext('2d')!, W = props.width, H = props.height, t = ms / 1000
  g.clearRect(0, 0, W, H)
  const lonC = 14 + 5 * Math.sin(t * 0.25)
  const G: GlobeStyle = { cx: W / 2, cy: H / 2 + 8, r: H * 0.45, spin: (-lonC * Math.PI) / 180, tilt: 0.52 }
  drawGlobe(g, G)

  const on = props.step >= props.arcAt
  if (on && !lastOn) arcT0 = t
  if (!on) arcT0 = -1
  lastOn = on
  const u = on ? (arcT0 < 0 ? 1 : Math.min(1, (t - arcT0) / 1.1)) : 0

  // the arc from ID to OOD, lifted off the surface
  if (u > 0) {
    const a = SITES.id.v, b = SITES.ood.v, N = 50, upto = Math.round(N * u)
    g.strokeStyle = OOD; g.lineWidth = 2.5; g.setLineDash([7, 5]); g.lineDashOffset = -t * 18
    g.beginPath()
    for (let i = 0; i <= upto; i++) {
      const f = i / N, lift = 1 + 0.18 * Math.sin(Math.PI * f)
      const v: Vec3 = [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f]
      const n = Math.hypot(...v), p = project([v[0] / n, v[1] / n, v[2] / n], G, lift)
      i ? g.lineTo(p.x, p.y) : g.moveTo(p.x, p.y)
    }
    g.stroke(); g.setLineDash([])
  }
  site(g, G, 'id', ID, t, 1, 1)
  // clamp to [0, 1]: canvas silently ignores a globalAlpha above 1 (e.g. 1.0000000000000002 from rounding),
  // which let the pulsing ring's alpha leak onto the whole OOD site and made it blink
  site(g, G, 'ood', OOD, t, Math.min(1, Math.max(0, (u - 0.7) / 0.3)), -1)
}

onMounted(() => { if (canvas.value) setupCanvas(canvas.value, props.width, props.height); raf = requestAnimationFrame(frame) })
onUnmounted(() => cancelAnimationFrame(raf))
</script>

<template>
  <canvas ref="canvas" :style="{ width: `${width}px`, height: `${height}px`, display: 'block' }" aria-label="Globe marking the Kahramanmaraş (ID) and Al Haouz (OOD) earthquakes" />
</template>
