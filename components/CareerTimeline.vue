<script setup lang="ts">
// Career journey from data/career.json. One stop per click; latest stop is emphasised.
// Slide: `clicks: <number of stops>`, :step="$clicks".
import { computed } from 'vue'
import career from '../data/career.json'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 99 })
const KIND: Record<string, string> = {
  industry: '#0072B2', research: '#56B4E9', academia: '#009E73', humanitarian: '#CC79A7', next: '#D55E00',
}
const stops = computed(() => career.stops.map((s, i) => ({
  ...s, i, shown: props.step >= i + 1, current: Math.min(props.step, career.stops.length) === i + 1,
})))
const isTodo = (s: string) => s?.startsWith('TODO')
const progress = computed(() => Math.min(1, Math.max(0, (props.step - 1) / Math.max(1, career.stops.length - 1))))
</script>

<template>
  <div class="tl">
    <div class="rail"><div class="fill" :style="{ width: progress * 100 + '%' }" /></div>
    <div class="stops" :style="{ gridTemplateColumns: `repeat(${career.stops.length}, 1fr)` }">
      <div v-for="s in stops" :key="s.i" class="stop" :class="{ shown: s.shown, current: s.current }">
        <div class="dot" :style="{ background: KIND[s.kind] || '#888' }" />
        <div class="when" :class="{ todo: isTodo(s.when) }">{{ s.when }}</div>
        <div class="org">{{ s.org }}</div>
        <div class="role" :class="{ todo: isTodo(s.role) }">{{ s.role }}</div>
        <div class="line" :class="{ todo: isTodo(s.line) }">{{ s.line }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tl { position: relative; margin-top: 36px; }
.rail { position: absolute; top: 9px; left: 5%; right: 5%; height: 3px; background: var(--rule); }
.fill { height: 100%; background: var(--ink); transition: width 600ms ease; }
.stops { display: grid; gap: 6px; position: relative; }
.stop { text-align: center; opacity: 0; transform: translateY(10px); transition: all 500ms ease; }
.stop.shown { opacity: 0.55; transform: none; }
.stop.current { opacity: 1; }
.stop.current .dot { transform: scale(1.5); box-shadow: 0 0 0 5px rgba(0,0,0,0.08); }
.dot { width: 20px; height: 20px; border-radius: 50%; margin: 0 auto 10px; border: 3px solid white; transition: transform 400ms; }
.when { font-size: 11px; color: var(--muted); font-weight: 700; }
.org { font-size: 14px; font-weight: 700; line-height: 1.15; margin-top: 2px; }
.role { font-size: 11px; line-height: 1.2; margin-top: 4px; }
.line { font-size: 11px; line-height: 1.2; margin-top: 6px; font-style: italic; color: #374151; }
.todo { background: #fff3a8; color: #6b5300; border-radius: 3px; }
</style>
