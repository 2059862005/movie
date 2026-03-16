<template>
  <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-8">
    <button
      @click="$emit('update:modelValue', modelValue - 1)"
      :disabled="modelValue <= 1"
      class="px-4 py-2 rounded-lg bg-gray-800 text-white hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>

    <div class="flex gap-1">
      <button
        v-for="page in visiblePages"
        :key="page"
        @click="$emit('update:modelValue', page)"
        :class="[
          'px-4 py-2 rounded-lg transition-colors',
          page === modelValue 
            ? 'bg-red-600 text-white' 
            : 'bg-gray-800 text-white hover:bg-gray-700'
        ]"
      >
        {{ page }}
      </button>
    </div>

    <button
      @click="$emit('update:modelValue', modelValue + 1)"
      :disabled="modelValue >= totalPages"
      class="px-4 py-2 rounded-lg bg-gray-800 text-white hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  },
  maxVisible: {
    type: Number,
    default: 5
  }
})

defineEmits(['update:modelValue'])

const visiblePages = computed(() => {
  const pages = []
  const { modelValue, totalPages, maxVisible } = props
  let start = Math.max(1, modelValue - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages, start + maxVisible - 1)
  
  if (end - start < maxVisible - 1) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})
</script>
