// A rotating dot globe for <canvas> (orthographic projection). Land = data/globe_land.json
// (Natural Earth 1:110m land, public domain, sampled on a Fibonacci sphere). Used by GlobeNetwork and ShiftingGlobe.
import land from '../data/globe_land.json'

export type Vec3 = [number, number, number]
const D2R = Math.PI / 180

// unit vector for [lon, lat] in degrees (y up, z toward the viewer at lon = 0)
export function lonLat(lon: number, lat: number): Vec3 {
  const l = lon * D2R, p = lat * D2R
  return [Math.cos(p) * Math.sin(l), Math.sin(p), Math.cos(p) * Math.cos(l)]
}

// rotate about y by `spin` (Earth turning), then tilt about x so we look from a little above the equator
export function view(v: Vec3, spin: number, tilt: number): Vec3 {
  const cs = Math.cos(spin), ss = Math.sin(spin)
  const x = v[0] * cs + v[2] * ss, z0 = -v[0] * ss + v[2] * cs
  const ct = Math.cos(tilt), st = Math.sin(tilt)
  return [x, v[1] * ct - z0 * st, v[1] * st + z0 * ct]
}

export const LAND: Vec3[] = (land.points as number[][]).map(([lon, lat]) => lonLat(lon, lat))

export interface GlobeStyle { cx: number; cy: number; r: number; spin: number; tilt: number; dot?: string; sea?: string; rim?: string }

// sphere, then the land dots on the near side (bigger and darker toward the viewer)
export function drawGlobe(g: CanvasRenderingContext2D, s: GlobeStyle, tint?: (v: Vec3, i: number) => string | null) {
  const grad = g.createRadialGradient(s.cx - s.r * 0.35, s.cy - s.r * 0.4, s.r * 0.1, s.cx, s.cy, s.r)
  grad.addColorStop(0, '#ffffff')
  grad.addColorStop(1, s.sea ?? '#e9eef4')
  g.beginPath(); g.arc(s.cx, s.cy, s.r, 0, Math.PI * 2)
  g.fillStyle = grad; g.fill()
  g.lineWidth = 1.5; g.strokeStyle = s.rim ?? '#c7cfd9'; g.stroke()
  for (let i = 0; i < LAND.length; i++) {
    const p = view(LAND[i], s.spin, s.tilt)
    if (p[2] <= 0.02) continue
    const c = tint?.(LAND[i], i) ?? null
    g.globalAlpha = c ? 1 : 0.35 + 0.65 * p[2]
    g.fillStyle = c ?? s.dot ?? '#4b5563'
    g.beginPath(); g.arc(s.cx + s.r * p[0], s.cy - s.r * p[1], (c ? 2.6 : 1.7) * (0.6 + 0.4 * p[2]), 0, Math.PI * 2); g.fill()
  }
  g.globalAlpha = 1
}

// screen position of a unit vector on (or above, k > 1) the globe, plus its depth
export function project(v: Vec3, s: GlobeStyle, k = 1): { x: number; y: number; z: number } {
  const p = view(v, s.spin, s.tilt)
  return { x: s.cx + s.r * k * p[0], y: s.cy - s.r * k * p[1], z: p[2] }
}

// set up a crisp canvas of logical size W x H; returns the 2D context
export function setupCanvas(c: HTMLCanvasElement, W: number, H: number, dpr = 2) {
  c.width = W * dpr; c.height = H * dpr
  const g = c.getContext('2d')!
  g.setTransform(dpr, 0, 0, dpr, 0, 0)
  return g
}
