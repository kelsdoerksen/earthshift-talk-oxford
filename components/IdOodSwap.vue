<script setup lang="ts">
import { asset } from '../utils/asset'
// Cross-fades an ID tile into its OOD counterpart.
// mode="step": OOD shows once `step >= at` (drive with :step="$clicks").
// mode="auto": loops ID <-> OOD every `interval` ms (good for galleries).
import { computed, onMounted, onUnmounted, ref } from 'vue'

const props = withDefaults(defineProps<{
  id: string
  ood: string
  idCaption?: string
  oodCaption?: string
  mode?: 'step' | 'auto'
  step?: number
  at?: number
  interval?: number
  size?: number
}>(), { mode: 'step', step: 99, at: 1, interval: 2200, size: 180 })

const tick = ref(false)
let timer: ReturnType<typeof setInterval> | undefined
onMounted(() => {
  if (props.mode === 'auto') timer = setInterval(() => { tick.value = !tick.value }, props.interval)
})
onUnmounted(() => timer && clearInterval(timer))

const showOod = computed(() => props.mode === 'auto' ? tick.value : props.step >= props.at)
const src = (name: string) => name.startsWith('/') || name.startsWith('http') ? asset(name) : asset(`/tiles/${name}.png`)
</script>

<template>
  <figure class="swap" :style="{ width: `${size}px` }">
    <div class="frame" :style="{ width: `${size}px`, height: `${size}px` }">
      <img :src="src(id)" class="layer" :class="{ hidden: showOod }" alt="in-distribution tile">
      <img :src="src(ood)" class="layer" :class="{ hidden: !showOod }" alt="out-of-distribution tile">
    </div>
    <figcaption v-if="idCaption || oodCaption">
      <span :class="showOod ? 'ood' : 'id'">{{ showOod ? oodCaption : idCaption }}</span>
    </figcaption>
  </figure>
</template>

<style scoped>
.swap { margin: 0; display: inline-flex; flex-direction: column; align-items: center; }
.frame { position: relative; }
.layer {
  position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
  transition: opacity 600ms ease, transform 600ms ease;
}
.layer.hidden { opacity: 0; transform: scale(0.97); }
figcaption { margin-top: 6px; font-size: 13px; text-align: center; min-height: 1.3em; }
</style>
