<template>
  <div class="min-h-screen pt-24 pb-12">
    <div class="container mx-auto px-4">
      <!-- Search Header -->
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-white mb-4">
          搜索结果: "{{ query }}"
        </h1>
        <p class="text-gray-400">
          找到 {{ store.totalResults }} 个结果
        </p>
      </div>

      <!-- Results -->
      <LoadingSpinner v-if="store.isLoading && store.searchResults.length === 0" />
      <ErrorMessage v-else-if="store.hasError" :message="store.error" @retry="doSearch" />
      
      <div v-else-if="store.searchResults.length === 0 && !store.isLoading" class="text-center py-12">
        <p class="text-gray-500 text-lg">没有找到相关电影</p>
      </div>

      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
        <MovieCard 
          v-for="movie in store.searchResults" 
          :key="movie.id" 
          :movie="movie"
        />
      </div>
      
      <!-- Load More -->
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
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import MovieCard from '@/components/MovieCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import Pagination from '@/components/common/Pagination.vue'
import ErrorMessage from '@/components/common/ErrorMessage.vue'

const route = useRoute()
const store = useMovieStore()

const currentPage = ref(1)
const query = computed(() => route.query.q || '')

const doSearch = () => {
  if (query.value) {
    store.searchMovies(query.value)
  }
}

const changePage = (page) => {
  currentPage.value = page
  store.searchMovies(query.value, page)
}

watch(query, () => {
  store.clearSearch()
  currentPage.value = 1
  doSearch()
})

onMounted(() => {
  if (query.value) {
    doSearch()
  }
})
</script>
