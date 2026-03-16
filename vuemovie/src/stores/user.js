import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/services/api'

export const useUserStore = defineStore('user', () => {
  const getStoredUser = () => {
    const stored = localStorage.getItem('user')
    return stored ? JSON.parse(stored) : null
  }

  const user = ref(getStoredUser())
  const token = ref(localStorage.getItem('token') || null)
  const profile = ref(null)
  
  const isLoggedIn = computed(() => !!user.value && !!token.value)
  const username = computed(() => user.value?.username || '')
  const avatar = computed(() => profile.value?.avatar || '')
  const isVip = computed(() => profile.value?.is_upgrade || false)
  const vipExpireTime = computed(() => profile.value?.expire_time || null)

  async function login(username, password) {
    const response = await authApi.login({ username, password })
    const { access } = response.data
    token.value = access
    localStorage.setItem('token', access)
    
    const userResponse = await authApi.getCurrentUser()
    user.value = userResponse.data
    profile.value = userResponse.data.profile
    localStorage.setItem('user', JSON.stringify(userResponse.data))
    
    return user.value
  }

  async function register(username, email, password) {
    await authApi.register({ username, email, password })
    return login(username, password)
  }

  async function fetchProfile() {
    if (!token.value) return
    try {
      const response = await authApi.getCurrentUser()
      user.value = response.data
      profile.value = response.data.profile
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (error) {
      console.error('获取用户信息失败', error)
    }
  }

  function logout() {
    user.value = null
    profile.value = null
    token.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    profile,
    isLoggedIn,
    username,
    avatar,
    isVip,
    vipExpireTime,
    login,
    register,
    logout,
    fetchProfile
  }
})
