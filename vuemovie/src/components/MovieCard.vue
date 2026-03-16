<template>
  <div 
    class="group cursor-pointer" 
    @click="goToDetail"
  >
    <div class="relative aspect-[2/3] rounded-xl overflow-hidden bg-gray-800 shadow-lg group-hover:shadow-2xl transition-all duration-300 group-hover:shadow-red-900/20">
      <!-- Image -->
      <img
        v-if="posterUrl"
        :src="posterUrl"
        :alt="movieTitle"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
        loading="lazy"
      />
      <!-- Placeholder -->
      <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
        </svg>
      </div>
      
      <!-- Score Badge -->
      <div class="absolute top-3 right-3 bg-black/80 backdrop-blur-sm px-2.5 py-1.5 rounded-lg flex items-center gap-1.5 shadow-lg">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
        <span class="text-white text-sm font-semibold">{{ movieScore }}</span>
      </div>
      
      <!-- Quality Badge -->
      <div v-if="movie.quality_display" class="absolute top-3 left-3 px-2 py-1 bg-red-600 text-white text-xs font-medium rounded">
        {{ movie.quality_display }}
      </div>
      
      <!-- Hover Overlay with Play Button -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="w-16 h-16 rounded-full bg-red-600/90 flex items-center justify-center transform scale-0 group-hover:scale-100 transition-transform duration-300 shadow-lg shadow-red-600/50">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
        <div class="absolute bottom-0 left-0 right-0 p-4">
          <p class="text-white text-sm line-clamp-3 font-light">{{ movieOverview }}</p>
        </div>
      </div>
    </div>
    
    <!-- Movie Info -->
    <div class="mt-4 space-y-1">
      <h3 class="text-white font-semibold truncate group-hover:text-red-500 transition-colors duration-200">
        {{ movieTitle }}
      </h3>
      <div class="flex items-center gap-2 text-gray-500 text-sm">
        <span>{{ movieYear }}</span>
        <span v-if="movie.Movie_area" class="text-gray-600">•</span>
        <span v-if="movie.Movie_area" class="text-gray-500">{{ movie.Movie_area }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { getImageUrl } from '@/services/api'

const props = defineProps({
  movie: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const movieTitle = computed(() => props.movie.Movie_name || props.movie.title || '')
const movieOverview = computed(() => props.movie.Movie_describe || props.movie.overview || '')
const movieScore = computed(() => props.movie.Movie_score || props.movie.vote_average || '0')
const movieYear = computed(() => {
  const date = props.movie.Movie_release_date || props.movie.release_date
  return date ? date.split('-')[0] : ''
})

const posterUrl = computed(() => {
  const path = props.movie.Movie_image || props.movie.poster_path
  return path ? getImageUrl(path) : ''
})

const goToDetail = () => {
  router.push({ name: 'MovieDetail', params: { id: props.movie.id } })
}
</script>
