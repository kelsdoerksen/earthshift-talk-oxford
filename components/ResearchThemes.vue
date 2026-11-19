<script setup lang="ts">
// Four research themes as cards with line icons, one per click (step >= i + 1).
// The operations card cites the npj Natural Hazards landslide paper (data/npj_numbers.json).
import npj from '../data/npj_numbers.json'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 99 })
const themes = [
  { key: 'gfm', title: 'Geospatial foundation models and satellite embeddings', color: '#2b7bd8' },
  { key: 'agri', title: 'Modelling climate impacts on agriculture', color: '#b8860b' },
  { key: 'bio', title: 'Biodiversity monitoring', color: '#2f8f5b', note: 'Research affiliate at NASA Jet Propulsion Lab using GFMs for forest canopy height mapping' },
  { key: 'ops', title: 'Building and deploying AI tools in operations', color: '#D55E00', note: 'e.g. sub-seasonal forecasting of monsoon-triggered landslide impacts in Nepal', cite: npj.citation, url: `https://doi.org/${npj.doi}` },
]
</script>

<template>
  <div class="themes">
    <div v-for="(th, i) in themes" :key="th.key" class="card" :class="{ on: step >= i + 1 }" :style="{ borderTopColor: th.color }">
      <svg width="46" height="46" viewBox="0 0 48 48" fill="none" :stroke="th.color" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" class="icon">
        <template v-if="th.key === 'gfm'">
          <rect x="17" y="6" width="10" height="8" rx="1.5" /><path d="M6 10h11M27 10h11M22 14v5" />
          <circle cx="22" cy="31" r="10" /><path d="M12 31h20M22 21c-4 4-4 16 0 20M22 21c4 4 4 16 0 20" />
          <path d="M38 24v18M42 30v12M34 34v8" stroke-width="3" />
        </template>
        <template v-else-if="th.key === 'agri'">
          <path d="M20 44V16" /><path d="M20 22c-6-1-8-6-8-9 5 0 8 3 8 9zM20 22c6-1 8-6 8-9-5 0-8 3-8 9zM20 32c-6-1-8-6-8-9 5 0 8 3 8 9zM20 32c6-1 8-6 8-9-5 0-8 3-8 9z" />
          <circle cx="38" cy="10" r="4" /><path d="M38 2v2M38 16v2M30 10h2M44 10h2M32.5 4.5l1.4 1.4M42.1 14.1l1.4 1.4M43.5 4.5l-1.4 1.4" />
        </template>
        <template v-else-if="th.key === 'bio'">
          <path d="M8 40c0-16 10-28 32-32-2 22-14 32-30 32" /><path d="M8 40l18-18" />
          <path d="M30 34c3-2 6-2 9 0M33 30c1.5 1.5 1.5 6 0 8" />
        </template>
        <template v-else>
          <circle cx="18" cy="26" r="6" /><path d="M18 14v4M18 34v4M6 26h4M26 26h4M9.5 17.5l2.8 2.8M23.7 31.7l2.8 2.8M9.5 34.5l2.8-2.8M23.7 20.3l2.8-2.8" />
          <path d="M32 8l8 8-8 8M40 16H28" /><path d="M30 40h12M36 34v12" />
        </template>
      </svg>
      <div class="t">{{ th.title }}</div>
      <div v-if="th.note" class="note">{{ th.note }}<template v-if="th.cite"><br><a :href="th.url" target="_blank" class="ref">{{ th.cite }}</a></template></div>
    </div>
  </div>
</template>

<style scoped>
.themes { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.card {
  background: #f6f7f8; border-top: 5px solid; border-radius: 8px; padding: 14px 16px; min-height: 128px;
  opacity: 0; transform: translateY(10px); transition: opacity 450ms, transform 450ms cubic-bezier(.2,.7,.2,1);
}
.card.on { opacity: 1; transform: none; }
.icon { display: block; margin-bottom: 8px; }
.t { font-weight: 700; font-size: 17px; line-height: 1.25; }
.note { font-size: 12.5px; color: var(--muted); margin-top: 6px; line-height: 1.35; }
.ref { color: var(--accent); font-weight: 600; }
</style>
