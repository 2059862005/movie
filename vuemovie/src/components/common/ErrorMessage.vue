<template>
  <div class="flex items-center justify-center py-12">
    <div class="flex flex-col items-center gap-4 text-center">
      <div class="w-16 h-16 rounded-full bg-red-500/20 flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <p class="text-gray-300 text-lg">{{ message || '加载失败' }}</p>
      <button 
        v-if="showRetry"
        @click="$emit('retry')"
        class="px-6 py-2 bg-primary text-white rounded-full hover:bg-red-600 transition-colors"
      >
        重试
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: ''
  },
  showRetry: {
    type: Boolean,
    default: true
  }
})

defineEmits(['retry'])
</script>
