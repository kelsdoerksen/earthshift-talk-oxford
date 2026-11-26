<script setup lang="ts">
import { asset } from '../utils/asset'
// What "in-distribution" and "out-of-distribution" mean, with static EarthShift tiles (FTW field boundaries).
// step 0: train on Germany → model · 1: ID test (Germany) + definition · 2: OOD test (Cambodia) + definition
// Static images; only fades on click. Default step 99 = everything shown.
const props = withDefaults(defineProps<{ step?: number }>(), { step: 99 })
</script>

<template>
  <div class="idood">
    <svg class="arrows" viewBox="0 0 868 380" width="868" height="380">
      <defs>
        <marker id="ah-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#1f2328" /></marker>
        <marker id="ah-id" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#0072B2" /></marker>
        <marker id="ah-ood" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#D55E00" /></marker>
      </defs>
      <path d="M176 190 H232" stroke="#1f2328" stroke-width="3" marker-end="url(#ah-ink)" />
      <path d="M372 175 C410 175, 410 105, 456 105" fill="none" stroke="#0072B2" stroke-width="3" marker-end="url(#ah-id)" class="fade" :class="{ on: step >= 1 }" />
      <path d="M372 205 C410 205, 410 285, 456 285" fill="none" stroke="#D55E00" stroke-width="3" marker-end="url(#ah-ood)" class="fade" :class="{ on: step >= 2 }" />
    </svg>

    <figure class="tile" style="left: 0; top: 108px">
      <img :src="asset('/tiles/ftw_germany_image_id.png')" width="164" alt="FTW Germany training tile">
      <figcaption><b>Train</b> on fields in Germany</figcaption>
    </figure>

    <div class="model" style="left: 240px; top: 150px">Model</div>

    <figure class="tile fade" :class="{ on: step >= 1 }" style="left: 466px; top: 40px">
      <img :src="asset('/tiles/ftw_germany_2018_id.png')" width="130" alt="FTW Germany test tile">
      <figcaption class="id">Test: more of Germany</figcaption>
    </figure>
    <figure class="tile fade" :class="{ on: step >= 2 }" style="left: 466px; top: 220px">
      <img :src="asset('/tiles/ftw_cambodia_image_ood.png')" width="130" alt="FTW Cambodia test tile">
      <figcaption class="ood">Test: Cambodia</figcaption>
    </figure>

    <div class="def fade" :class="{ on: step >= 1 }" style="top: 52px">
      <div class="id">In-distribution (ID)</div>
      Test data drawn from the <b>same distribution</b> as the training data: same places, time, sensor and processing.
    </div>
    <div class="def fade" :class="{ on: step >= 2 }" style="top: 232px">
      <div class="ood">Out-of-distribution (OOD)</div>
      Test data from a <b>shifted distribution</b>: what a model meets once it is deployed somewhere new.
    </div>
  </div>
</template>

<style scoped>
.idood { position: relative; width: 868px; height: 380px; margin: 14px auto 0; }
.arrows { position: absolute; inset: 0; }
.tile { position: absolute; margin: 0; text-align: center; }
.tile img { display: block; }
.tile figcaption { font-size: 14px; margin-top: 6px; }
.model {
  position: absolute; width: 132px; height: 80px; border: 3px solid var(--ink); border-radius: 12px;
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 20px; background: #fafaf8;
}
.def { position: absolute; left: 630px; width: 238px; font-size: 14.5px; line-height: 1.35; }
.def > div { font-size: 17px; margin-bottom: 4px; }
.fade { opacity: 0; transition: opacity 500ms ease; }
.fade.on { opacity: 1; }
</style>
