import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { movieApi } from '@/services/api'

export const useMovieStore = defineStore('movie', () => {
  const popularMovies = ref([])
  const nowPlayingMovies = ref([])
  const currentMovie = ref(null)
  const searchResults = ref([])
  const categories = ref([])
  const discoveredMovies = ref([])
  
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalResults = ref(0)
  
  const isLoading = ref(false)
  const error = ref(null)
  
  const searchQuery = ref('')
  const selectedCategory = ref(null)
  const selectedArea = ref(null)

  const hasMore = computed(() => currentPage.value < totalPages.value)
  const hasError = computed(() => error.value !== null)

  async function fetchPopularMovies(page = 1) {
    isLoading.value = true
    error.value = null
    try {
      const response = await movieApi.getMovies({ 
        Movie_is_hot: '1',
        page,
        Movie_is_show: '1'
      })
      const results = response.data.results || response.data
      if (page === 1) {
        popularMovies.value = results
      } else {
        popularMovies.value = [...popularMovies.value, ...results]
      }
      currentPage.value = response.data.next ? page + 1 : page
      totalPages.value = Math.ceil(response.data.count / 10) || 1
      totalResults.value = response.data.count || results.length
    } catch (e) {
      error.value = '获取热门电影失败'
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchNowPlayingMovies(page = 1) {
    isLoading.value = true
    error.value = null
    try {
      const response = await movieApi.getMovies({ 
        Movie_is_show: '1',
        ordering: '-Movie_release_date',
        page
      })
      const results = response.data.results || response.data
      if (page === 1) {
        nowPlayingMovies.value = results
      } else {
        nowPlayingMovies.value = [...nowPlayingMovies.value, ...results]
      }
      currentPage.value = response.data.next ? page + 1 : page
    } catch (e) {
      error.value = '获取电影列表失败'
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMovieDetail(movieId) {
    isLoading.value = true
    error.value = null
    currentMovie.value = null
    try {
      const response = await movieApi.getMovie(movieId)
      currentMovie.value = response.data
    } catch (e) {
      error.value = '获取电影详情失败'
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMoviePlay(movieId) {
    try {
      const response = await movieApi.getMoviePlay(movieId)
      return response.data
    } catch (e) {
      if (e.response?.status === 403) {
        throw new Error('VIP会员才能观看')
      }
      throw e
    }
  }

  async function searchMovies(query, page = 1) {
    if (!query.trim()) {
      searchResults.value = []
      return
    }
    searchQuery.value = query
    isLoading.value = true
    error.value = null
    try {
      const response = await movieApi.getMovies({ 
        search: query,
        page
      })
      const results = response.data.results || response.data
      if (page === 1) {
        searchResults.value = results
      } else {
        searchResults.value = [...searchResults.value, ...results]
      }
      currentPage.value = response.data.next ? page + 1 : page
    } catch (e) {
      error.value = '搜索失败'
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchCategories() {
    try {
      const response = await movieApi.getCategories()
      categories.value = response.data.results || response.data
    } catch (e) {
      console.error(e)
    }
  }

  async function fetchDiscoverMovies(categoryId, area, page = 1, year = null) {
    isLoading.value = true
    error.value = null
    try {
      const params = { page }
      if (categoryId) params.Movie_category = categoryId
      if (area) params.Movie_area = area
      if (year) params.Movie_release_date__year = year
      
      const response = await movieApi.getMovies(params)
      const results = response.data.results || response.data
      if (page === 1) {
        discoveredMovies.value = results
      } else {
        discoveredMovies.value = [...discoveredMovies.value, ...results]
      }
      currentPage.value = response.data.next ? page + 1 : page
    } catch (e) {
      error.value = '获取电影列表失败'
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  async function collectMovie(movieId) {
    const response = await movieApi.collectMovie(movieId)
    return response.data.status
  }

  async function wishMovie(movieId) {
    const response = await movieApi.wishMovie(movieId)
    return response.data.status
  }

  async function watchingMovie(movieId) {
    const response = await movieApi.watchingMovie(movieId)
    return response.data.status
  }

  async function watchedMovie(movieId) {
    const response = await movieApi.watchedMovie(movieId)
    return response.data.status
  }

  async function getMyCollections() {
    const response = await movieApi.getMyCollections()
    return response.data
  }

  async function getMyWishes() {
    const response = await movieApi.getMyWishes()
    return response.data
  }

  async function getMyWatching() {
    const response = await movieApi.getMyWatching()
    return response.data
  }

  async function getMyWatched() {
    const response = await movieApi.getMyWatched()
    return response.data
  }

  function clearSearch() {
    searchResults.value = []
    searchQuery.value = ''
    currentPage.value = 1
  }

  return {
    popularMovies,
    nowPlayingMovies,
    currentMovie,
    searchResults,
    categories,
    discoveredMovies,
    currentPage,
    totalPages,
    totalResults,
    isLoading,
    error,
    searchQuery,
    selectedCategory,
    selectedArea,
    hasMore,
    hasError,
    fetchPopularMovies,
    fetchNowPlayingMovies,
    fetchMovieDetail,
    fetchMoviePlay,
    searchMovies,
    fetchCategories,
    fetchDiscoverMovies,
    collectMovie,
    wishMovie,
    watchingMovie,
    watchedMovie,
    getMyCollections,
    getMyWishes,
    getMyWatching,
    getMyWatched,
    clearSearch
  }
})
