<template>
  <div v-if="video" class="relative aspect-video rounded-lg overflow-hidden bg-black">
    <iframe
      :src="`https://www.youtube.com/embed/${video.key}?autoplay=1`"
      title="Trailer"
      class="w-full h-full"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen
    ></iframe>
  </div>
  <div v-else class="aspect-video rounded-lg bg-gray-800 flex items-center justify-center">
    <p class="text-gray-500">暂无预告片</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  videos: {
    type: Array,
    default: () => []
  }
})

// 获取官方预告片
const video = computed(() => {
  if (!props.videos || props.videos.length === 0) return null
  
  // 优先查找预告片
  const trailer = props.videos.find(v => 
    v.type === 'Trailer' && v.site === 'YouTube' && v.official
  )
  if (trailer) return trailer
  
  // 然后查找任何预告片
  const anyTrailer = props.videos.find(v => 
    v.type === 'Trailer' && v.site === 'YouTube'
  )
  if (anyTrailer) return anyTrailer
  
  // 最后返回第一个 YouTube 视频
  return props.videos.find(v => v.site === 'YouTube')
})
</script>
