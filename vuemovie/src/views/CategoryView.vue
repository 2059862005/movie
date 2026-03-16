<template>
  <div class="min-h-screen pt-24 pb-12">
    <div class="container mx-auto px-4">
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-white mb-4">
          {{ categoryName }}
        </h1>
        <p class="text-gray-400">
          共 {{ store.totalResults }} 部电影
        </p>
      </div>

      <div class="flex flex-wrap gap-4 mb-8">
        <select 
          v-model="selectedGenre"
          @change="applyFilters"
          class="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-primary"
        >
          <option :value="null">所有类型</option>
          <option v-for="genre in store.categories" :key="genre.id" :value="genre.id">
            {{ genre.name }}
          </option>
        </select>

        <select 
          v-model="selectedYear"
          @change="applyFilters"
          class="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-primary"
        >
          <option :value="null">所有年份</option>
          <option v-for="year in years" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>

      <LoadingSpinner v-if="store.isLoading && store.discoveredMovies.length === 0" />
      <ErrorMessage v-else-if="store.hasError" :message="store.error" @retry="applyFilters" />
      
      <div v-else-if="store.discoveredMovies.length === 0 && !store.isLoading" class="text-center py-12">
        <p class="text-gray-500 text-lg">该分类下暂无电影</p>
      </div>

      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
        <MovieCard 
          v-for="movie in store.discoveredMovies" 
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import MovieCard from '@/components/MovieCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import Pagination from '@/components/common/Pagination.vue'
import ErrorMessage from '@/components/common/ErrorMessage.vue'

const route = useRoute()
const store = useMovieStore()

const selectedGenre = ref(null)
const selectedYear = ref(null)
const currentPage = ref(1)

const years = Array.from({ length: 30 }, (_, i) => new Date().getFullYear() - i)

const categoryName = computed(() => {
  const genreId = parseInt(route.params.id)
  const genre = (store.categories || []).find(g => g.id === genreId)
  return genre ? genre.name : '电影分类'
})

const applyFilters = () => {
  currentPage.value = 1
  store.fetchDiscoverMovies(
    selectedGenre.value || undefined,
    undefined,
    1,
    selectedYear.value || undefined
  )
}

const changePage = (page) => {
  currentPage.value = page
  store.fetchDiscoverMovies(
    selectedGenre.value || undefined,
    undefined,
    page,
    selectedYear.value || undefined
  )
}

onMounted(async () => {
  await store.fetchCategories()
  
  const genreId = parseInt(route.params.id)
  if (genreId) {
    const categoryExists = store.categories.some(c => c.id === genreId)
    if (categoryExists) {
      selectedGenre.value = genreId
    }
  }
  
  applyFilters()
})

watch(() => route.params.id, () => {
  const genreId = parseInt(route.params.id)
  const categoryExists = store.categories.some(c => c.id === genreId)
  selectedGenre.value = (genreId && categoryExists) ? genreId : null
  applyFilters()
})
</script>

