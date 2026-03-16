<template>
  <div class="min-h-screen pt-16">
    <div v-if="movie" class="relative h-[40vh] md:h-[50vh]">
      <div class="absolute inset-0">
        <img
          :src="backdropUrl"
          :alt="movieTitle"
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-dark via-dark/80 to-transparent"></div>
      </div>
    </div>

    <div class="relative -mt-32 container mx-auto px-4">
      <LoadingSpinner v-if="store.isLoading && !movie" />
      <ErrorMessage v-else-if="store.hasError" :message="store.error" @retry="fetchDetail" />
      
      <div v-else-if="movie" class="grid md:grid-cols-[300px_1fr] gap-8">
        <div class="hidden md:block">
          <img
            :src="posterUrl"
            :alt="movieTitle"
            class="w-full rounded-lg shadow-xl"
          />
        </div>

        <div class="space-y-6">
          <div>
            <h1 class="text-3xl md:text-4xl font-bold text-white mb-2">
              {{ movieTitle }}
            </h1>
            <p v-if="movie.Movie_type" class="text-gray-400">
              {{ movie.Movie_type }}
            </p>
          </div>

          <div class="flex flex-wrap items-center gap-4">
            <span class="flex items-center gap-1 text-yellow-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              {{ movieScore }} ({{ movie.Movie_douban_score || '0' }} 豆瓣)
            </span>
            <span class="text-gray-400">{{ movie.Movie_duration }} 分钟</span>
            <span class="text-gray-400">{{ movie.Movie_release_date }}</span>
            <span v-if="movie.quality_display" class="text-gray-400">{{ movie.quality_display }}</span>
          </div>

          <div class="flex flex-wrap gap-2">
            <span class="px-3 py-1 bg-gray-800 rounded-full text-sm text-gray-300">
              {{ categoryName }}
            </span>
          </div>

          <div>
            <h3 class="text-xl font-bold text-white mb-2">简介</h3>
            <p class="text-gray-300 leading-relaxed">
              {{ movieOverview || '暂无简介' }}
            </p>
          </div>

          <div class="flex flex-wrap gap-4">
            <button 
              @click="goToPlay"
              class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
              </svg>
              立即播放
            </button>
            <button 
              @click="handleCollect"
              class="px-6 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              {{ collectText }}
            </button>
            <button 
              @click="handleWish"
              class="px-6 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              {{ wishText }}
            </button>
          </div>

          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-gray-400">导演：</span>
              <span class="text-white">{{ movie.Movie_director || '-' }}</span>
            </div>
            <div>
              <span class="text-gray-400">编剧：</span>
              <span class="text-white">{{ movie.scriptwriter || '-' }}</span>
            </div>
            <div>
              <span class="text-gray-400">主演：</span>
              <span class="text-white">{{ movie.Movie_actor || '-' }}</span>
            </div>
            <div>
              <span class="text-gray-400">地区：</span>
              <span class="text-white">{{ movie.region_display || movie.Movie_area || '-' }}</span>
            </div>
            <div>
              <span class="text-gray-400">语言：</span>
              <span class="text-white">{{ movie.Movie_language || '-' }}</span>
            </div>
            <div>
              <span class="text-gray-400">字幕：</span>
              <span class="text-white">{{ movie.Movie_subtitle || '-' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import { getImageUrl } from '@/services/api'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorMessage from '@/components/common/ErrorMessage.vue'

const route = useRoute()
const router = useRouter()
const store = useMovieStore()

const collectText = ref('收藏')
const wishText = ref('想看')

const movie = computed(() => store.currentMovie)
const movieTitle = computed(() => movie.value?.Movie_name || movie.value?.title || '')
const movieOverview = computed(() => movie.value?.Movie_describe || movie.value?.overview || '')
const movieScore = computed(() => movie.value?.Movie_score || movie.value?.vote_average || '0')
const categoryName = computed(() => movie.value?.category_name || movie.value?.Movie_category || '')
const posterUrl = computed(() => {
  const path = movie.value?.Movie_image || movie.value?.poster_path
  return path ? getImageUrl(path) : ''
})
const backdropUrl = computed(() => {
  const path = movie.value?.Movie_image || movie.value?.backdrop_path
  return path ? getImageUrl(path) : posterUrl.value
})

const fetchDetail = () => {
  store.fetchMovieDetail(route.params.id)
}

const goToPlay = () => {
  router.push({ name: 'Play', params: { id: route.params.id } })
}

const handleCollect = async () => {
  try {
    const status = await store.collectMovie(route.params.id)
    collectText.value = status === '收藏成功' ? '已收藏' : '收藏'
  } catch (e) {
    alert('请先登录')
    router.push('/login')
  }
}

const handleWish = async () => {
  try {
    const status = await store.wishMovie(route.params.id)
    wishText.value = status === '想看成功' ? '已想看' : '想看'
  } catch (e) {
    alert('请先登录')
    router.push('/login')
  }
}

onMounted(() => {
  fetchDetail()
})
</script>
