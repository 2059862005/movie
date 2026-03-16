<template>
  <div class="min-h-screen pt-16">
    <!-- Hero Banner -->
    <section v-if="store.nowPlayingMovies.length > 0" class="relative h-[60vh] md:h-[75vh] overflow-hidden">
      <!-- Background Image with Parallax-like Effect -->
      <div class="absolute inset-0">
        <img
          :src="getImageUrl(store.nowPlayingMovies[0].Movie_image)"
          :alt="store.nowPlayingMovies[0].Movie_name"
          class="w-full h-full object-cover scale-105"
        />
        <!-- Multi-layer Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-r from-dark via-dark/80 to-transparent"></div>
        <div class="absolute inset-0 bg-gradient-to-t from-dark via-transparent to-transparent"></div>
        <div class="absolute inset-0 bg-dark/20"></div>
      </div>
      
      <!-- Animated Content -->
      <div class="relative container mx-auto px-4 h-full flex items-center">
        <div class="max-w-3xl" :key="store.nowPlayingMovies[0].id">
          <!-- Badge -->
          <div class="flex items-center gap-3 mb-4 animate-fade-in-up">
            <span class="px-3 py-1 bg-red-600 text-white text-sm font-medium rounded-full">
              正在热映
            </span>
            <span class="flex items-center gap-1 text-yellow-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              {{ formatScore(store.nowPlayingMovies[0].Movie_score) }}
            </span>
          </div>
          
          <!-- Title -->
          <h1 class="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-4 animate-fade-in-up delay-100">
            {{ store.nowPlayingMovies[0].Movie_name }}
          </h1>
          
          <!-- Overview -->
          <p class="text-gray-300 text-lg md:text-xl line-clamp-3 mb-6 max-w-2xl animate-fade-in-up delay-200">
            {{ store.nowPlayingMovies[0].Movie_describe }}
          </p>
          
          <!-- Meta Info -->
          <div class="flex flex-wrap items-center gap-4 mb-8 text-gray-400 animate-fade-in-up delay-300">
            <span class="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ store.nowPlayingMovies[0].Movie_release_date }}
            </span>
            <span v-if="store.nowPlayingMovies[0].Movie_duration">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ store.nowPlayingMovies[0].Movie_duration }} 分钟
            </span>
          </div>
          
          <!-- Action Buttons -->
          <div class="flex flex-wrap gap-4 animate-fade-in-up delay-400">
            <button 
              @click="goToPlay(store.nowPlayingMovies[0].id)"
              class="group px-8 py-4 bg-red-600 text-white font-semibold rounded-xl hover:bg-red-700 transition-all duration-300 flex items-center gap-3 shadow-lg shadow-red-600/30 hover:shadow-red-600/50 hover:scale-105"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 group-hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              立即播放
            </button>
            <button 
              @click="goToDetail(store.nowPlayingMovies[0].id)"
              class="group px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-xl hover:bg-white/20 transition-all duration-300 flex items-center gap-3 border border-white/20 hover:border-white/40"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              详情
            </button>
          </div>
        </div>
      </div>
      
      <!-- Scroll Indicator -->
      <div class="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white/50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </div>
    </section>

    <!-- Popular Movies -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between mb-10">
          <div class="flex items-center gap-4">
            <div class="w-1 h-8 bg-red-600 rounded-full"></div>
            <h2 class="text-3xl font-bold text-white">热门电影</h2>
          </div>
        </div>
        
        <LoadingSpinner v-if="store.isLoading && store.popularMovies.length === 0" />
        <ErrorMessage v-else-if="store.hasError" :message="store.error" @retry="store.fetchPopularMovies()" />
        
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
          <MovieCard 
            v-for="movie in store.popularMovies" 
            :key="movie.id" 
            :movie="movie"
          />
        </div>
        
        <Pagination 
          v-if="store.totalPages > 1"
          v-model="currentPage" 
          :total-pages="store.totalPages"
          @update:modelValue="changePage"
        />
      </div>
    </section>

    <!-- Now Playing -->
    <section class="py-16 bg-gradient-to-b from-gray-900/50 to-transparent">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between mb-10">
          <div class="flex items-center gap-4">
            <div class="w-1 h-8 bg-red-600 rounded-full"></div>
            <h2 class="text-3xl font-bold text-white">正在上映</h2>
          </div>
        </div>
        
        <LoadingSpinner v-if="store.isLoading && store.nowPlayingMovies.length === 0" />
        
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
          <MovieCard 
            v-for="movie in store.nowPlayingMovies" 
            :key="movie.id" 
            :movie="movie"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import { getImageUrl } from '@/services/api'
import MovieCard from '@/components/MovieCard.vue'
import Pagination from '@/components/common/LoadingSpinner.vue'
import ErrorMessage from '@/components/common/ErrorMessage.vue'

const router = useRouter()
const store = useMovieStore()
const currentPage = ref(1)

onMounted(() => {
  store.fetchPopularMovies()
  store.fetchNowPlayingMovies()
})

const changePage = (page) => {
  currentPage.value = page
  store.fetchPopularMovies(page)
}

const formatScore = (score) => {
  if (!score) return '0.0'
  const num = parseFloat(score)
  return isNaN(num) ? '0.0' : num.toFixed(1)
}

const goToPlay = (id) => {
  router.push({ name: 'Play', params: { id } })
}

const goToDetail = (id) => {
  router.push({ name: 'MovieDetail', params: { id } })
}
</script>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out forwards;
}

.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }
.delay-300 { animation-delay: 0.3s; }
.delay-400 { animation-delay: 0.4s; }
</style>
