<template>
  <header 
    class="fixed top-0 left-0 right-0 z-50 transition-all duration-300"
    :class="[
      isScrolled ? 'bg-dark/95 backdrop-blur-md shadow-lg shadow-black/20' : 'bg-transparent',
      isScrolled ? 'py-2' : 'py-4'
    ]"
  >
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Left Section -->
        <div class="flex items-center gap-8">
          <!-- Logo -->
          <router-link to="/" class="flex items-center gap-2 group">
            <div class="w-10 h-10 bg-gradient-to-br from-red-600 to-red-700 rounded-xl flex items-center justify-center shadow-lg shadow-red-600/30 group-hover:scale-105 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
              </svg>
            </div>
            <span class="text-xl font-bold text-white group-hover:text-red-500 transition-colors">MovieHub</span>
          </router-link>

          <!-- Desktop Navigation -->
          <nav class="hidden md:flex items-center gap-1">
            <router-link 
              to="/" 
              class="px-4 py-2 text-gray-300 hover:text-white hover:bg-white/5 rounded-lg transition-all"
              :class="{ 'text-white bg-white/10': $route.path === '/' }"
            >
              棣栭〉
            </router-link>
            <router-link 
              to="/category/28" 
              class="px-4 py-2 text-gray-300 hover:text-white hover:bg-white/5 rounded-lg transition-all"
              :class="{ 'text-white bg-white/10': $route.path.startsWith('/category') }"
            >
              鐢靛奖
            </router-link>
          </nav>
        </div>

        <!-- Right Section -->
        <div class="flex items-center gap-3">
          <!-- Desktop Search -->
          <div class="relative hidden sm:block">
            <input
              type="text"
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              placeholder="鎼滅储鐢靛奖..."
              class="w-48 md:w-64 px-4 py-2 bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-full text-white placeholder-gray-500 focus:outline-none focus:border-red-500 focus:bg-gray-800 focus:w-56 md:focus:w-72 transition-all"
            />
            <button
              @click="handleSearch"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>

          <!-- Mobile Search Button -->
          <button 
            @click="mobileSearchOpen = true"
            class="sm:hidden p-2 text-gray-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>

          <!-- User Menu -->
          <div v-if="userStore.isLoggedIn" class="relative group">
            <button class="flex items-center gap-2 text-gray-300 hover:text-white transition-colors">
              <div class="w-9 h-9 rounded-full bg-gradient-to-br from-red-600 to-red-700 flex items-center justify-center shadow-lg shadow-red-600/30">
                <span class="text-white font-medium">{{ userStore.username.charAt(0).toUpperCase() }}</span>
              </div>
              <span class="hidden sm:block">{{ userStore.username }}</span>
            </button>
            <!-- Dropdown -->
            <div class="absolute right-0 mt-2 w-56 bg-gray-800/95 backdrop-blur-xl rounded-xl shadow-2xl border border-gray-700/50 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform origin-top-right">
              <div class="py-2"><router-link to="/profile" class="w-full px-4 py-3 text-left text-gray-300 hover:bg-white/5 hover:text-white transition-colors flex items-center gap-3"><svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>个人中心</router-link><router-link to="/vip" class="w-full px-4 py-3 text-left text-gray-300 hover:bg-white/5 hover:text-white transition-colors flex items-center gap-3"><svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>VIP会员</router-link><div class="my-1 border-t border-gray-700"></div><button @click="handleLogout"
                  class="w-full px-4 py-3 text-left text-gray-300 hover:bg-white/5 hover:text-white transition-colors flex items-center gap-3"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  閫€鍑虹櫥褰?                </button>
              </div>
            </div>
          </div>

          <!-- Login/Register -->
          <div v-else class="flex items-center gap-2">
            <router-link
              to="/login"
              class="px-4 py-2 text-gray-300 hover:text-white transition-colors hidden sm:block"
            >
              鐧诲綍
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 bg-gradient-to-r from-red-600 to-red-700 text-white rounded-lg hover:from-red-500 hover:to-red-600 transition-all shadow-lg shadow-red-600/30"
            >
              娉ㄥ唽
            </router-link>
          </div>

          <!-- Mobile Menu Button -->
          <button 
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-2 text-gray-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
          >
            <svg v-if="!mobileMenuOpen" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <Transition name="slide">
      <div v-if="mobileMenuOpen" class="md:hidden bg-gray-900/95 backdrop-blur-md border-t border-gray-800">
        <nav class="container mx-auto px-4 py-4 space-y-2">
          <router-link 
            to="/" 
            @click="mobileMenuOpen = false"
            class="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
          >
            棣栭〉
          </router-link>
          <router-link 
            to="/category/28" 
            @click="mobileMenuOpen = false"
            class="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
          >
            鐢靛奖
          </router-link>
          <div v-if="!userStore.isLoggedIn" class="pt-2 space-y-2">
            <router-link 
              to="/login" 
              @click="mobileMenuOpen = false"
              class="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
            >
              鐧诲綍
            </router-link>
            <router-link 
              to="/register" 
              @click="mobileMenuOpen = false"
              class="block px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 text-white text-center rounded-lg"
            >
              娉ㄥ唽
            </router-link>
          </div>
        </nav>
      </div>
    </Transition>

    <!-- Mobile Search Overlay -->
    <Transition name="fade">
      <div v-if="mobileSearchOpen" class="md:hidden fixed inset-0 z-50 bg-dark/95 backdrop-blur-md">
        <div class="container mx-auto px-4 pt-20">
          <div class="relative">
            <input
              type="text"
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              autofocus
              placeholder="鎼滅储鐢靛奖..."
              class="w-full px-4 py-4 bg-gray-800 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-red-500"
            />
            <button
              @click="mobileSearchOpen = false"
              class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const searchQuery = ref('')
const isScrolled = ref(false)
const mobileMenuOpen = ref(false)
const mobileSearchOpen = ref(false)

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ 
      name: 'Search', 
      query: { q: searchQuery.value } 
    })
    searchQuery.value = ''
    mobileSearchOpen.value = false
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/')
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>


