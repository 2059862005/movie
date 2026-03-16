<template>
  <div class="min-h-screen pt-16 bg-gray-900">
    <div class="container mx-auto px-4 py-8">
      <div class="flex flex-col md:flex-row gap-6">
        <aside class="w-full md:w-64 bg-gray-800 rounded-lg p-6">
          <div class="text-center mb-6">
            <div class="w-24 h-24 mx-auto rounded-full bg-gray-700 flex items-center justify-center mb-4">
              <span class="text-4xl text-gray-400">{{ userStore.username?.charAt(0).toUpperCase() }}</span>
            </div>
            <h2 class="text-xl font-bold text-white">{{ userStore.username }}</h2>
            <p class="text-gray-400 text-sm">{{ userStore.user?.email }}</p>
            <div v-if="userStore.isVip" class="mt-2 inline-block px-3 py-1 bg-yellow-600 text-white text-xs rounded-full">
              VIP会员 至 {{ formatDate(userStore.profile?.expire_time) }}
            </div>
          </div>
          <nav class="space-y-2">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'w-full text-left px-4 py-2 rounded-lg transition-colors',
                activeTab === tab.id ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
          <button 
            @click="handleLogout"
            class="w-full mt-6 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            退出登录
          </button>
        </aside>

        <main class="flex-1 bg-gray-800 rounded-lg p-6">
          <h2 class="text-2xl font-bold text-white mb-6">{{ tabs.find(t => t.id === activeTab)?.name }}</h2>
          
          <LoadingSpinner v-if="isLoading" />
          
          <div v-else-if="currentList.length === 0" class="text-center text-gray-400 py-12">
            <p>暂无内容</p>
          </div>
          
          <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
            <MovieCard 
              v-for="movie in currentList" 
              :key="movie.id" 
              :movie="movie"
            />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useMovieStore } from '@/stores/movie'
import MovieCard from '@/components/MovieCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const router = useRouter()
const userStore = useUserStore()
const movieStore = useMovieStore()

const activeTab = ref('collections')
const isLoading = ref(false)
const collections = ref([])
const wishes = ref([])
const watching = ref([])
const watched = ref([])

const tabs = [
  { id: 'collections', name: '我的收藏' },
  { id: 'wishes', name: '想看' },
  { id: 'watching', name: '在看' },
  { id: 'watched', name: '看过' }
]

const currentList = computed(() => {
  switch (activeTab.value) {
    case 'collections': return collections.value
    case 'wishes': return wishes.value
    case 'watching': return watching.value
    case 'watched': return watched.value
    default: return []
  }
})

async function loadData() {
  isLoading.value = true
  try {
    const promises = [
      movieStore.getMyCollections(),
      movieStore.getMyWishes(),
      movieStore.getMyWatching(),
      movieStore.getMyWatched()
    ]
    const [col, wish, watch, watchd] = await Promise.all(promises)
    collections.value = col
    wishes.value = wish
    watching.value = watch
    watched.value = watchd
  } catch (error) {
    console.error('加载数据失败', error)
  } finally {
    isLoading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

function handleLogout() {
  userStore.logout()
  router.push('/')
}

watch(activeTab, () => {
  loadData()
})

onMounted(() => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  userStore.fetchProfile()
  loadData()
})
</script>
