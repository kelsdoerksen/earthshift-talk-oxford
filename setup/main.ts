import { defineAppSetup } from '@slidev/types'
import { asset } from '../utils/asset'

// Makes $asset('/figures/x.png') available in slide markdown (pages/*.md).
export default defineAppSetup(({ app }) => {
  app.config.globalProperties.$asset = asset
})
