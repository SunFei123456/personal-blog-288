<script setup lang="ts">
/**
 * 404 页面
 */

import { RouterLink } from 'vue-router'
import { Home, ArrowLeft } from 'lucide-vue-next'
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center">
      <h1 class="text-9xl font-bold text-gray-200">404</h1>
      <h2 class="text-2xl font-semibold text-gray-900 mt-4">页面不存在</h2>
      <p class="text-gray-600 mt-2">抱歉，您访问的页面不存在或已被删除</p>
      <div class="flex items-center justify-center gap-4 mt-8">
        <button
          @click="$router.back()"
          class="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <ArrowLeft class="w-4 h-4" />
          返回上页
        </button>
        <RouterLink
          to="/"
          class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Home class="w-4 h-4" />
          返回首页
        </RouterLink>
      </div>
    </div>
  </div>
</template>
