<script setup lang="ts">
// Table 1 of the paper, revealed one shift type per click (data/datasets.csv).
// Slide: `clicks: 5`, :step="$clicks". Pass `focus="Geographic"` to highlight one group.
import { computed } from 'vue'
import raw from '../data/datasets.csv?raw'
import { parseCsv, SHIFT_COLORS } from '../utils/csv'

const props = withDefaults(defineProps<{ step?: number; focus?: string }>(), { step: 99 })
const ORDER = ['Scale', 'Temporal', 'Geographic', 'Sensor', 'Processing']
const groups = computed(() => {
  const rows = parseCsv(raw)
  return ORDER.map((s, i) => ({
    shift: s, i, on: props.step >= i + 1,
    rows: rows.filter(r => r.shift === s),
    cases: rows.filter(r => r.shift === s).reduce((n, r) => n + (r.bidirectional === 'true' ? 2 : 1), 0),
  }))
})
const n = (v: string) => Number(v).toLocaleString('en-US')
</script>

<template>
  <table class="ds">
    <thead><tr><th>Shift</th><th>Task</th><th>ID → OOD</th><th class="r">Train</th><th class="r">OOD test</th></tr></thead>
    <tbody v-for="g in groups" :key="g.shift" :class="{ on: g.on, dim: focus && focus !== g.shift }">
      <tr v-for="(r, j) in g.rows" :key="r.pair">
        <td v-if="j === 0" :rowspan="g.rows.length" class="shift" :style="{ borderLeftColor: SHIFT_COLORS[g.shift] }">
          {{ g.shift }}<div class="cases">{{ g.cases }} test cases</div>
        </td>
        <td class="task">{{ r.task }}</td>
        <td>{{ r.pair }}</td>
        <td class="r">{{ n(r.train) }}</td>
        <td class="r">{{ n(r.ood) }}</td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.ds { font-size: 11.5px; border-collapse: collapse; width: 100%; }
.ds th { text-align: left; font-size: 11px; color: var(--muted); border-bottom: 2px solid var(--ink); padding: 3px 8px; }
.ds td { padding: 2px 8px; border-bottom: 1px solid #eef0f2; }
.r { text-align: right; font-variant-numeric: tabular-nums; }
.shift { font-weight: 700; border-left: 5px solid; vertical-align: top; }
.cases { font-weight: 400; font-size: 10px; color: var(--muted); }
.task { color: var(--muted); }
tbody { opacity: 0.08; transition: opacity 500ms; }
tbody.on { opacity: 1; }
tbody.on.dim { opacity: 0.3; }
</style>
