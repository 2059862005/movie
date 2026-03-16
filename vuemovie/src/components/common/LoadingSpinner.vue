<template>
  <div class="flex items-center justify-center py-12">
    <div class="flex flex-col items-center gap-4">
      <div class="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      <p class="text-gray-400">{{ message || '加载中...' }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: ''
  }
})
</script>
