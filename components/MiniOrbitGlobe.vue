<script setup lang="ts">
// A small turning dot-globe with a few satellites in near-polar orbits (a schematic constellation).
// Real-time loop; orbits are illustrative, not real satellite tracks.
import { onMounted, onUnmounted, ref } from 'vue'
import { drawGlobe, setupCanvas, type GlobeStyle, type Vec3 } from '../utils/globe'

const props = withDefaults(defineProps<{ size?: number; sats?: number }>(), { size: 130, sats: 6 })
const canvas = ref<HTMLCanvasElement>()
let raf = 0

function frame(ms: number) {
  raf = requestAnimationFrame(frame)
  const c = canvas.value
  if (!c || c.offsetParent === null) return
  const g = c.getContext('2d')!, S = props.size, t = ms / 1000
  g.clearRect(0, 0, S, S)
  const G: GlobeStyle = { cx: S / 2, cy: S / 2, r: S * 0.32, spin: t * 0.25, tilt: 0.35 }
  const ORB = 1.35
  // near-polar orbit planes, spread in longitude (sun-synchronous-ish look)
  const planes = Array.from({ length: 3 }, (_, k) => {
    const rot = k * 1.05 + 0.4, inc = 1.45
    const A: Vec3 = [Math.cos(rot), 0, Math.sin(rot)]
    const B: Vec3 = [-Math.sin(rot) * Math.cos(inc), Math.sin(inc), Math.cos(rot) * Math.cos(inc)]
    return { A, B }
  })
  const pos = (k: number) => {
    const P = planes[k % 3], a = t * 0.9 + (k * 2 * Math.PI) / props.sats + k * 0.3
    const c2 = Math.cos(a), s2 = Math.sin(a)
    const p: Vec3 = [c2 * P.A[0] + s2 * P.B[0], c2 * P.A[1] + s2 * P.B[1], c2 * P.A[2] + s2 * P.B[2]]
    return { x: G.cx + G.r * ORB * p[0], y: G.cy - G.r * ORB * p[1], z: p[2] }
  }
  const sats = Array.from({ length: props.sats }, (_, k) => pos(k))
  const dot = (s: { x: number; y: number }) => { g.fillStyle = '#2b7bd8'; g.fillRect(s.x - 4, s.y - 1.5, 8, 3); g.fillStyle = '#1f2328'; g.fillRect(s.x - 1.8, s.y - 1.8, 3.6, 3.6) }
  sats.forEach(s => { if (s.z < 0 && Math.hypot(s.x - G.cx, s.y - G.cy) > G.r) dot(s) })
  drawGlobe(g, G)
  sats.forEach(s => { if (s.z >= 0) dot(s) })
}

onMounted(() => { if (canvas.value) setupCanvas(canvas.value, props.size, props.size); raf = requestAnimationFrame(frame) })
onUnmounted(() => cancelAnimationFrame(raf))
</script>

<template>
  <canvas ref="canvas" :style="{ width: `${size}px`, height: `${size}px`, display: 'block' }" aria-label="Earth with satellites orbiting" />
</template>
