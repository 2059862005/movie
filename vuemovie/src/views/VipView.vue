<template>
  <div class="min-h-screen pt-16 bg-gray-900">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-white text-center mb-4">开通VIP会员</h1>
      <p class="text-gray-400 text-center mb-8">开通VIP，畅享全站电影</p>

      <div v-if="userStore.isVip" class="bg-yellow-600/20 border border-yellow-600 rounded-lg p-6 mb-8 text-center">
        <h2 class="text-2xl font-bold text-yellow-500 mb-2">您已是VIP会员</h2>
        <p class="text-gray-300">有效期至：{{ formatDate(userStore.profile?.expire_time) }}</p>
      </div>

      <LoadingSpinner v-if="isLoading" />
      
      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <div 
          v-for="card in vipCards" 
          :key="card.id"
          class="bg-gray-800 rounded-lg p-6 text-center hover:transform hover:scale-105 transition-transform"
        >
          <h3 class="text-xl font-bold text-white mb-2">{{ card.card_name }}</h3>
          <div class="text-4xl font-bold text-yellow-500 mb-4">
            ¥{{ card.card_price }}
          </div>
          <p class="text-gray-400 mb-6">{{ card.duration }}天</p>
          <p v-if="card.info" class="text-sm text-gray-500 mb-6">{{ card.info }}</p>
          <button 
            @click="handleBuy(card.id)"
            class="w-full py-3 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors"
          >
            立即开通
          </button>
        </div>
      </div>

      <div class="mt-12 max-w-2xl mx-auto">
        <h3 class="text-xl font-bold text-white mb-4">VIP特权</h3>
        <ul class="space-y-3 text-gray-400">
          <li class="flex items-center gap-2">
            <span class="text-yellow-500">✓</span>
            畅享全站所有付费电影
          </li>
          <li class="flex items-center gap-2">
            <span class="text-yellow-500">✓</span>
            4K超清画质体验
          </li>
          <li class="flex items-center gap-2">
            <span class="text-yellow-500">✓</span>
            专属VIP客服服务
          </li>
          <li class="flex items-center gap-2">
            <span class="text-yellow-500">✓</span>
            会员专属活动
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { vipApi, paymentApi } from '@/services/api'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const userStore = useUserStore()
const vipCards = ref([])
const isLoading = ref(false)

async function loadVipCards() {
  isLoading.value = true
  try {
    const response = await vipApi.getVipCards()
    vipCards.value = response.data.results || response.data
  } catch (error) {
    console.error('获取VIP卡失败', error)
  } finally {
    isLoading.value = false
  }
}

async function handleBuy(cardId) {
  if (!userStore.isLoggedIn) {
    window.location.href = '/login'
    return
  }
  
  try {
    const response = await paymentApi.createOrder(cardId)
    const { pay_url } = response.data
    window.location.href = pay_url
  } catch (error) {
    alert('创建订单失败: ' + (error.response?.data?.detail || error.message))
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadVipCards()
})
</script>
