<script setup lang="ts">
// Subtle animated satellite ground tracks for the cover / section slides.
const tracks = [0, 1, 2, 3, 4].map(i => ({
  d: Array.from({ length: 121 }, (_, k) => {
    const x = k * 10
    const yv = 300 + 190 * Math.sin((x / 1200) * Math.PI * 2 + i * 1.25)
    return `${k ? 'L' : 'M'}${x},${yv.toFixed(1)}`
  }).join(' '),
  delay: i * 1.6,
}))
</script>

<template>
  <svg class="orbits" viewBox="0 0 1200 600" preserveAspectRatio="none" aria-hidden="true">
    <defs>
      <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
        <circle cx="2" cy="2" r="1.2" fill="#c9ced6" />
      </pattern>
    </defs>
    <rect width="1200" height="600" fill="url(#dots)" opacity="0.6" />
    <g v-for="(t, i) in tracks" :key="i">
      <path :d="t.d" class="track" />
      <circle r="5" class="sat" :class="i % 2 ? 'ood-sat' : 'id-sat'">
        <animateMotion :dur="`${14 + i * 2}s`" :begin="`${t.delay}s`" repeatCount="indefinite" :path="t.d" />
      </circle>
    </g>
  </svg>
</template>

<style scoped>
.orbits { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; }
.track { fill: none; stroke: #c2c8d0; stroke-width: 1.2; stroke-dasharray: 4 6; }
.id-sat { fill: var(--id); }
.ood-sat { fill: var(--ood); }
</style>
