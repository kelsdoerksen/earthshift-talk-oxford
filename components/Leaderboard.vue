<script setup lang="ts">
// A ranked leaderboard that can fill and then drain to "?" rows.
// step < growAt: empty rows (ranks only) · step >= growAt: bars grow, last row first, #1 turns ink
// step >= drainAt: bars shrink back top-first and each row becomes a "?".
// Data: data/state_of_geoai.json (coding_leaderboard). Default step 99 = drained (the slide's final state).
import { computed } from 'vue'
import facts from '../data/state_of_geoai.json'

const props = withDefaults(defineProps<{ step?: number; growAt?: number; drainAt?: number; max?: number }>(),
  { step: 99, growAt: 1, drainAt: 2, max: 100 })

const rows = facts.coding_leaderboard.rows
const grown = computed(() => props.step >= props.growAt && props.step < props.drainAt)
const drained = computed(() => props.step >= props.drainAt)
const n = rows.length
</script>

<template>
  <div class="board">
    <div v-for="(r, i) in rows" :key="r.rank" class="row">
      <div class="rank">{{ r.rank }}</div>
      <div class="name" :style="{ opacity: grown ? 1 : 0, transitionDelay: grown ? `${(n - 1 - i) * 140}ms` : `${i * 110}ms` }">{{ r.model }}</div>
      <div class="track" :class="{ gone: drained }" :style="{ transitionDelay: `${i * 110 + 250}ms` }">
        <div
          class="bar" :class="{ first: i === 0 && grown }"
          :style="{
            width: grown ? `${(r.score / max) * 100}%` : '0%',
            transitionDelay: grown ? `${(n - 1 - i) * 140}ms` : `${i * 110}ms`,
          }"
        />
      </div>
      <div class="val" :style="{ opacity: grown ? 1 : 0, transitionDelay: grown ? `${(n - 1 - i) * 140 + 450}ms` : `${i * 110}ms` }">{{ r.score }}</div>
      <div class="ask" :style="{ opacity: drained ? 1 : 0, transitionDelay: drained ? `${i * 110 + 420}ms` : '0ms' }">?</div>
    </div>
  </div>
</template>

<style scoped>
.board { width: 760px; margin: 22px auto 0; border: 1px solid var(--rule); border-radius: 8px; background: #fafaf8; }
.row { position: relative; display: flex; align-items: center; height: 58px; padding: 0 22px; border-top: 1px solid var(--rule); }
.row:first-child { border-top: none; }
.rank { width: 32px; font-size: 15px; color: var(--muted); font-variant-numeric: tabular-nums; }
.name { width: 230px; font-size: 21px; font-weight: 600; transition: opacity 350ms; }
.track { flex: 1; height: 16px; background: #ebe9e4; border-radius: 3px; overflow: hidden; transition: opacity 300ms; }
.track.gone { opacity: 0; }
.bar { height: 100%; background: #9db3d9; transition: width 750ms cubic-bezier(.2,.7,.2,1), background 400ms 900ms; }
.bar.first { background: var(--ink); }
.val { width: 60px; text-align: right; font-size: 18px; font-variant-numeric: tabular-nums; transition: opacity 300ms; }
.ask { position: absolute; left: 50%; font-size: 26px; font-weight: 600; transform: translateX(-50%); transition: opacity 300ms; pointer-events: none; }
</style>
