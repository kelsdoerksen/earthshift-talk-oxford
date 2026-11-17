// Minimal CSV parser for the small data files in /data (no quoted commas needed).
export function parseCsv(raw: string): Record<string, string>[] {
  const lines = raw.trim().split(/\r?\n/).filter(l => l.trim().length)
  if (lines.length < 2) return []
  const header = lines[0].split(',').map(h => h.trim())
  return lines.slice(1).map((line) => {
    const cells = line.split(',')
    const row: Record<string, string> = {}
    header.forEach((h, i) => { row[h] = (cells[i] ?? '').trim() })
    return row
  })
}

// Linear scale helper: maps domain [d0,d1] to range [r0,r1]
export function scale(d0: number, d1: number, r0: number, r1: number) {
  return (v: number) => r0 + ((v - d0) / (d1 - d0)) * (r1 - r0)
}

export function ticks(d0: number, d1: number, step: number): number[] {
  const out: number[] = []
  const start = Math.ceil(d0 / step) * step
  for (let v = start; v <= d1 + 1e-9; v += step) out.push(Math.round(v * 1000) / 1000)
  return out
}

export const SHIFT_COLORS: Record<string, string> = {
  Temporal: '#56B4E9',
  Scale: '#0072B2',
  Geographic: '#009E73',
  Processing: '#CC79A7',
  Sensor: '#D55E00',
}

export const FAMILY_COLORS: Record<string, string> = {
  GFM: 'var(--gfm)',
  VFM: 'var(--vfm)',
  Random: 'var(--rnd)',
  Other: '#888',
}
