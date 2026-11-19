<script setup lang="ts">
// EarthShift opener: a dot-globe rocks gently; the training region (ID, blue) sits on it. On the right, the data
// distribution of that region (blue curve) and of where the model is used (orange curve). In a loop, the orange
// curve slides away from the blue one, once per EarthShift shift type (named in its SHIFT_COLORS colour); for the
// geographic shift an arc flies from the ID region to the OOD region on the globe, for the others the ID region
// itself turns orange ("same place, different data").
// ILLUSTRATION ONLY: curve offsets and widths are not results.
import { onMounted, onUnmounted, ref } from 'vue'
import { drawGlobe, lonLat, project, setupCanvas, type GlobeStyle, type Vec3 } from '../utils/globe'
import { SHIFT_COLORS } from '../utils/csv'

const W = 980, H = 552
const canvas = ref<HTMLCanvasElement>()
let raf = 0
const ID = '#0072B2', OOD = '#D55E00', INK = '#1f2328', MUTED = '#6b7280'
const FONT = '"Liberation Sans", Helvetica, Arial, sans-serif'

const G: GlobeStyle = { cx: 255, cy: 352, r: 165, spin: 0, tilt: 0.42 }
const HOME = { lon: 10, lat: 51 }                 // FTW Germany (the ID region)
const AWAY = { lon: 105, lat: 12.5 }              // FTW Cambodia (the geographic OOD region)
const home = lonLat(HOME.lon, HOME.lat), away = lonLat(AWAY.lon, AWAY.lat)
const near = (v: Vec3, c: Vec3, cos: number) => v[0] * c[0] + v[1] * c[1] + v[2] * c[2] > cos

const SHIFTS = [
  { name: 'Temporal', what: 'same place, another year', sig: 38 },
  { name: 'Scale', what: 'same scene, another resolution', sig: 30 },
  { name: 'Geographic', what: 'another place', sig: 46 },
  { name: 'Sensor', what: 'same place, another sensor', sig: 52 },
  { name: 'Processing', what: 'same scene, another processing level', sig: 36 },
]
const CYCLE = 4.6
const PX0 = 545, PX1 = 950, BASE = 452, PEAK = 150, MU = 650, SHIFT = 150, SIG_ID = 40
const ease = (u: number) => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u))

function curve(g: CanvasRenderingContext2D, mu: number, sig: number, color: string, alpha: number) {
  g.beginPath(); g.moveTo(PX0, BASE)
  for (let x = PX0; x <= PX1; x += 3) g.lineTo(x, BASE - PEAK * Math.exp(-((x - mu) ** 2) / (2 * sig * sig)) * (SIG_ID / sig) ** 0.5)
  g.lineTo(PX1, BASE); g.closePath()
  g.globalAlpha = 0.16 * alpha; g.fillStyle = color; g.fill()
  g.globalAlpha = alpha; g.lineWidth = 3; g.strokeStyle = color; g.stroke(); g.globalAlpha = 1
}

// text with a white halo so it stays readable over the globe's dots
function halo(g: CanvasRenderingContext2D, text: string, x: number, y: number, color: string, align: CanvasTextAlign = 'left') {
  g.textAlign = align; g.textBaseline = 'middle'; g.lineJoin = 'round'
  g.lineWidth = 5; g.strokeStyle = 'rgba(255,255,255,0.92)'; g.strokeText(text, x, y)
  g.fillStyle = color; g.fillText(text, x, y)
}

function frame(ms: number) {
  raf = requestAnimationFrame(frame)
  const c = canvas.value
  if (!c || c.offsetParent === null) return
  const g = c.getContext('2d')!
  const t = ms / 1000
  g.clearRect(0, 0, W, H)

  const k = Math.floor(t / CYCLE) % SHIFTS.length, S = SHIFTS[k], u = (t % CYCLE) / CYCLE
  const out = ease((u - 0.12) / 0.3) * (1 - ease((u - 0.88) / 0.12))   // 0 = overlapping, 1 = fully shifted
  const geo = S.name === 'Geographic'

  // the globe rocks between the two regions (spin = -longitude faces that longitude)
  const lonC = 52 + 16 * Math.sin(t * 0.22)
  G.spin = (-lonC * Math.PI) / 180
  drawGlobe(g, G, (v) => {
    if (near(v, home, 0.988)) return geo || out < 0.5 ? ID : OOD
    if (geo && near(v, away, 0.99)) return out > 0.5 ? OOD : null
    return null
  })

  // labels on the globe
  const ph = project(home, G), pa = project(away, G)
  g.font = `700 14px ${FONT}`; g.textBaseline = 'middle'
  if (ph.z > 0) {
    g.strokeStyle = ID; g.lineWidth = 2; g.beginPath(); g.arc(ph.x, ph.y, 20, 0, Math.PI * 2); g.stroke()
    halo(g, 'training region (ID)', ph.x + 28, ph.y - 10, ID)
    if (!geo && out > 0.05) {
      g.globalAlpha = out; g.strokeStyle = OOD; g.lineWidth = 3
      g.beginPath(); g.arc(ph.x, ph.y, 20 + 10 * out, 0, Math.PI * 2); g.stroke()
      halo(g, S.what, ph.x + 28, ph.y + 14, OOD); g.globalAlpha = 1
    }
  }
  // geographic: an arc over the globe from home to away
  if (geo && ph.z > 0 && pa.z > 0) {
    const N = 48, pts: { x: number; y: number }[] = []
    for (let i = 0; i <= N; i++) {
      const f = i / N, lift = 1 + 0.32 * Math.sin(Math.PI * f)
      const v: Vec3 = [home[0] + (away[0] - home[0]) * f, home[1] + (away[1] - home[1]) * f, home[2] + (away[2] - home[2]) * f]
      const n = Math.hypot(...v)
      pts.push(project([v[0] / n, v[1] / n, v[2] / n], G, lift))
    }
    const shown = Math.round(N * ease(out * 1.4))
    g.strokeStyle = OOD; g.lineWidth = 2.5; g.setLineDash([6, 5]); g.lineDashOffset = -t * 20
    g.beginPath(); pts.slice(0, shown + 1).forEach((p, i) => (i ? g.lineTo(p.x, p.y) : g.moveTo(p.x, p.y))); g.stroke()
    g.setLineDash([])
    if (out > 0.6) {
      g.globalAlpha = (out - 0.6) / 0.4
      g.strokeStyle = OOD; g.lineWidth = 2; g.beginPath(); g.arc(pa.x, pa.y, 18, 0, Math.PI * 2); g.stroke()
      halo(g, 'deployment region (OOD)', pa.x - 24, pa.y + 30, OOD, 'right'); g.globalAlpha = 1
    }
  }

  // distributions
  g.strokeStyle = '#c7cfd9'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(PX0, BASE); g.lineTo(PX1, BASE); g.stroke()
  g.font = `500 13px ${FONT}`; g.fillStyle = MUTED; g.textAlign = 'right'; g.textBaseline = 'top'
  g.fillText('what the images look like →', PX1, BASE + 8)
  const muO = MU + SHIFT * out
  curve(g, MU, SIG_ID, ID, 1)
  curve(g, muO, S.sig, OOD, 0.35 + 0.65 * Math.min(1, out * 2))
  g.font = `700 15px ${FONT}`; g.textBaseline = 'alphabetic'
  g.fillStyle = ID; g.textAlign = 'right'; g.fillText('training data (ID)', MU - 18, BASE - PEAK - 12)
  g.globalAlpha = Math.min(1, out * 2); g.fillStyle = OOD; g.textAlign = 'center'; g.fillText('deployment data (OOD)', Math.min(muO, PX1 - 86), BASE - PEAK * (SIG_ID / S.sig) ** 0.5 - 12)
  // the shift arrow and its name
  if (out > 0.15) {
    const y = BASE - PEAK * 1.16 - 48, x0 = MU, x1 = muO
    g.strokeStyle = INK; g.fillStyle = INK; g.lineWidth = 2
    g.beginPath(); g.moveTo(x0, y); g.lineTo(x1 - 8, y); g.stroke()
    g.beginPath(); g.moveTo(x1, y); g.lineTo(x1 - 10, y - 6); g.lineTo(x1 - 10, y + 6); g.closePath(); g.fill()
    g.font = `700 20px ${FONT}`; g.fillStyle = SHIFT_COLORS[S.name]; g.textAlign = 'center'
    g.fillText(`${S.name} shift`, (x0 + x1) / 2, y - 14)
  }
  g.globalAlpha = 1
}

onMounted(() => { if (canvas.value) setupCanvas(canvas.value, W, H); raf = requestAnimationFrame(frame) })
onUnmounted(() => cancelAnimationFrame(raf))
</script>

<template>
  <canvas ref="canvas" class="shift-globe" aria-label="A training region on a globe; its data distribution and a deployment distribution that keeps shifting away" />
</template>

<style scoped>
.shift-globe { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; }
</style>
