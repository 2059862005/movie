<template>
  <div class="min-h-screen pt-16 bg-gray-900">
    <LoadingSpinner v-if="isLoading" />
    
    <div v-else-if="error" class="container mx-auto px-4 py-12 text-center">
      <p class="text-red-500 text-xl mb-4">{{ error }}</p>
      <button 
        v-if="error.includes('VIP')"
        @click="$router.push('/vip')"
        class="px-6 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700"
      >
        开通VIP
      </button>
    </div>
    
    <div v-else-if="movie">
      <div class="bg-black">
        <div class="container mx-auto px-4 py-4">
          <h1 class="text-white text-xl">{{ movie.Movie_name }}</h1>
        </div>
      </div>

      <div class="container mx-auto px-4 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div class="lg:col-span-2">
            <div class="bg-gray-800 rounded-lg p-4 mb-6">
              <h3 class="text-white font-bold mb-2">网盘信息</h3>
              <div v-if="movie.Movie_Storage" class="space-y-2">
                <div 
                  v-for="(line, index) in movie.Movie_Storage.split('\\n')" 
                  :key="index"
                  class="text-gray-300 text-sm"
                >
                  <span v-if="line.includes('百度网盘')" class="text-blue-400 font-bold">百度网盘：</span>
                  <span v-else-if="line.includes('提取码')" class="text-green-400 font-bold">提取码：</span>
                  <a v-if="line.includes('http')" :href="line.match(/http[^\s]+/)?.[0]" target="_blank" class="text-blue-300 underline">
                    {{ line.match(/http[^\s]+/)?.[0] }}
                  </a>
                  <span v-else>{{ line }}</span>
                </div>
              </div>
              <p v-else class="text-gray-500">暂无网盘信息</p>
            </div>

            <div class="bg-gray-800 rounded-lg p-4">
              <h3 class="text-white font-bold mb-4">电影简介</h3>
              <p class="text-gray-300 leading-relaxed">{{ movie.Movie_describe || '暂无简介' }}</p>
            </div>
          </div>

          <div>
            <div class="bg-gray-800 rounded-lg p-4">
              <h3 class="text-white font-bold mb-4">电影信息</h3>
              <div class="space-y-3 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-400">导演</span>
                  <span class="text-white">{{ movie.Movie_director || '-' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-400">编剧</span>
                  <span class="text-white">{{ movie.scriptwriter || '-' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-400">主演</span>
                  <span class="text-white">{{ movie.Movie_actor || '-' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-400">类型</span>
                  <span class="text-white">{{ movie.Movie_type || '-' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-400">地区</span>
                  <span class="text-white">{{ movie.region_display || movie.Movie_area || '-' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-400">语言</span>
                  <span class="text-white">{{ movie.Movie_language || '-' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-400">上映日期</span>
                  <span class="text-white">{{ movie.Movie_release_date || '-' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-400">片长</span>
                  <span class="text-white">{{ movie.Movie_duration || '-' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-400">评分</span>
                  <span class="text-yellow-500">{{ movie.Movie_score || '-' }}</span>
                </div>
              </div>
            </div>

            <div class="mt-4 space-y-2">
              <button 
                @click="handleCollect"
                class="w-full py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600"
              >
                {{ collectStatus || '收藏' }}
              </button>
              <button 
                @click="handleWish"
                class="w-full py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600"
              >
                {{ wishStatus || '想看' }}
              </button>
              <button 
                @click="handleWatching"
                class="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                {{ watchingStatus || '标记在看' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const route = useRoute()
const movieStore = useMovieStore()

const movie = ref(null)
const isLoading = ref(true)
const error = ref(null)
const collectStatus = ref(null)
const wishStatus = ref(null)
const watchingStatus = ref(null)

async function loadMovie() {
  isLoading.value = true
  error.value = null
  
  try {
    const movieId = route.params.id
    await movieStore.fetchMovieDetail(movieId)
    movie.value = movieStore.currentMovie
    
    if (!movie.value) {
      error.value = '电影不存在'
    }
  } catch (e) {
    if (e.message === 'VIP会员才能观看') {
      error.value = 'VIP会员才能观看此电影'
    } else {
      error.value = '加载失败'
    }
  } finally {
    isLoading.value = false
  }
}

async function handleCollect() {
  try {
    const status = await movieStore.collectMovie(movie.value.id)
    collectStatus.value = status
  } catch (e) {
    alert('操作失败')
  }
}

async function handleWish() {
  try {
    const status = await movieStore.wishMovie(movie.value.id)
    wishStatus.value = status
  } catch (e) {
    alert('操作失败')
  }
}

async function handleWatching() {
  try {
    const status = await movieStore.watchingMovie(movie.value.id)
    watchingStatus.value = status
  } catch (e) {
    alert('操作失败')
  }
}

onMounted(() => {
  loadMovie()
})
</script>
