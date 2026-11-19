<script setup lang="ts">
// A wall of quote cards, one per GFM paper: model · year, and a verbatim abstract excerpt with
// "state-of-the-art" / "SoTA" swept by a highlighter. Cards arrive when step >= cardsAt (staggered),
// and the last cell asks "Which one is best?" when step >= askAt.
// Data: data/state_of_geoai.json (sota_quotes). Default step 99 = all shown.
import { computed } from 'vue'
import facts from '../data/state_of_geoai.json'

const props = withDefaults(defineProps<{ step?: number; cardsAt?: number; askAt?: number; countAt?: number }>(),
  { step: 99, cardsAt: 0, askAt: 1, countAt: 1 })
const count = facts.gfm_count

const quotes = facts.sota_quotes.quotes.map((q) => {
  const m = q.excerpt.match(/(.*?)(state-of-the-art|SoTA)(.*)/)
  return { ...q, pre: m ? m[1] : q.excerpt, hit: m ? m[2] : '', post: m ? m[3] : '' }
})
const showCards = computed(() => props.step >= props.cardsAt)
const showAsk = computed(() => props.step >= props.askAt)
</script>

<template>
  <div class="wall">
    <div
      v-for="(q, k) in quotes" :key="q.model" class="card" :class="{ on: showCards }"
      :style="{ transitionDelay: showCards ? `${k * 120}ms` : '0ms' }"
    >
      <div class="head"><b>{{ q.model }}</b> · {{ q.year }}</div>
      <div class="body">{{ q.pre }}<mark :class="{ on: showCards }" :style="{ transitionDelay: showCards ? `${k * 120 + 350}ms` : '0ms' }">{{ q.hit }}</mark>{{ q.post }}</div>
    </div>
    <div class="ask" :class="{ on: showAsk }">Which one is best?</div>
  </div>
  <div class="count" :class="{ on: step >= countAt }">
    <b>{{ count.label }}</b> geospatial foundation models to choose from, and growing
  </div>
</template>

<style scoped>
.wall { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px 12px; margin-top: 14px; }
.card {
  padding: 9px 12px; border: 2px solid var(--ink); border-radius: 8px; background: #fafaf8; min-height: 92px;
  opacity: 0; transform: translateY(10px); transition: opacity 300ms, transform 300ms cubic-bezier(.2,.7,.2,1);
}
.card.on { opacity: 1; transform: none; }
.head { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 12px; color: var(--muted); }
.head b { color: var(--ink); font-weight: 600; }
.body { margin-top: 5px; font-size: 14px; line-height: 1.3; }
mark {
  color: inherit; white-space: nowrap; padding: 0 2px; margin: 0 -2px; border-radius: 3px;
  background: linear-gradient(#bfe3a0, #bfe3a0) no-repeat 0 0 / 0% 100%;
  transition: background-size 450ms ease-out;
}
mark.on { background-size: 100% 100%; }
.ask {
  display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 700;
  opacity: 0; transition: opacity 500ms;
}
.ask.on { opacity: 1; }
.count { margin-top: 12px; text-align: center; font-size: 19px; opacity: 0; transition: opacity 500ms 300ms; }
.count.on { opacity: 1; }
</style>
