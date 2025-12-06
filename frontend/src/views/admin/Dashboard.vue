<script setup lang="ts">
/**
 * 后台控制台页面
 * - 统计数据展示
 * - 快捷操作入口
 */

import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { getStatisticsApi } from '@/api/admin'
import type { Statistics } from '@/types'
import { Users, FileText, Eye, Plus, Settings } from 'lucide-vue-next'

/** 统计数据 */
const statistics = ref<Statistics>({
  user_count: 0,
  article_count: 0,
  view_count: 0,
})
const loading = ref(true)

/**
 * 获取统计数据
 */
async function fetchStatistics() {
  try {
    statistics.value = await getStatisticsApi()
  } catch (error) {
    console.error('获取统计数据失败:', error)
  } finally {
    loading.value = false
  }
}

/** 统计卡片配置 */
const statCards = [
  { key: 'user_count', label: '用户总数', icon: Users, color: 'blue' },
  { key: 'article_count', label: '文章总数', icon: FileText, color: 'green' },
  { key: 'view_count', label: '总浏览量', icon: Eye, color: 'orange' },
]

/** 快捷操作 */
const quickActions = [
  { path: '/admin/articles/edit', label: '写文章', icon: Plus },
  { path: '/admin/articles', label: '管理文章', icon: FileText },
  { path: '/admin/categories', label: '管理分类', icon: Settings },
]

// 初始化
onMounted(fetchStatistics)
</script>

<template>
  <div>
    <!-- 页面标题 -->
    <h1 class="text-2xl font-bold text-gray-900 mb-8 tracking-tight">控制台</h1>

    <!-- 欢迎信息 -->
    <div class="mb-8 bg-gradient-to-br from-indigo-600 to-violet-600 rounded-2xl p-8 text-white shadow-lg shadow-indigo-200">
      <h2 class="text-2xl font-bold mb-2">欢迎使用个人博客管理系统</h2>
      <p class="text-indigo-100">在这里您可以管理您的文章、评论、分类和标签。</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div
        v-for="card in statCards"
        :key="card.key"
        class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-all duration-300 transform hover:-translate-y-1"
      >
        <div class="flex items-center justify-between mb-4">
          <div
            class="w-12 h-12 rounded-xl flex items-center justify-center transition-colors"
            :class="{
              'bg-blue-50 text-blue-600': card.color === 'blue',
              'bg-green-50 text-green-600': card.color === 'green',
              'bg-purple-50 text-purple-600': card.color === 'purple',
              'bg-orange-50 text-orange-600': card.color === 'orange',
            }"
          >
            <component :is="card.icon" class="w-6 h-6" />
          </div>
          <span class="text-xs font-medium px-2.5 py-0.5 rounded-full" 
            :class="{
              'bg-blue-50 text-blue-600': card.color === 'blue',
              'bg-green-50 text-green-600': card.color === 'green',
              'bg-purple-50 text-purple-600': card.color === 'purple',
              'bg-orange-50 text-orange-600': card.color === 'orange',
            }">
            +12%
          </span>
        </div>
        <div>
          <p class="text-sm text-gray-500 font-medium">{{ card.label }}</p>
          <p class="text-3xl font-bold text-gray-900 mt-1 tracking-tight">
            {{ loading ? '-' : statistics[card.key as keyof Statistics] }}
          </p>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
      <h2 class="text-lg font-bold text-gray-900 mb-6">快捷操作</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <RouterLink
          v-for="action in quickActions"
          :key="action.path"
          :to="action.path"
          class="group flex flex-col items-center gap-3 p-6 bg-gray-50 rounded-xl hover:bg-indigo-50 hover:text-indigo-600 transition-all border border-transparent hover:border-indigo-100"
        >
          <div class="w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center group-hover:scale-110 transition-transform">
            <component :is="action.icon" class="w-5 h-5 text-gray-400 group-hover:text-indigo-500" />
          </div>
          <span class="font-medium text-gray-700 group-hover:text-indigo-700">{{ action.label }}</span>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
