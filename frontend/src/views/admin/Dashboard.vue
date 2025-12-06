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
import { Users, FileText, MessageSquare, Eye, Plus, Settings } from 'lucide-vue-next'

/** 统计数据 */
const statistics = ref<Statistics>({
  user_count: 0,
  article_count: 0,
  comment_count: 0,
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
  { key: 'comment_count', label: '评论总数', icon: MessageSquare, color: 'purple' },
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
    <h1 class="text-2xl font-bold text-gray-900 mb-6">控制台</h1>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div
        v-for="card in statCards"
        :key="card.key"
        class="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">{{ card.label }}</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">
              {{ loading ? '-' : statistics[card.key as keyof Statistics] }}
            </p>
          </div>
          <div
            class="w-12 h-12 rounded-full flex items-center justify-center"
            :class="{
              'bg-blue-100 text-blue-600': card.color === 'blue',
              'bg-green-100 text-green-600': card.color === 'green',
              'bg-purple-100 text-purple-600': card.color === 'purple',
              'bg-orange-100 text-orange-600': card.color === 'orange',
            }"
          >
            <component :is="card.icon" class="w-6 h-6" />
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">快捷操作</h2>
      <div class="flex flex-wrap gap-4">
        <RouterLink
          v-for="action in quickActions"
          :key="action.path"
          :to="action.path"
          class="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg hover:bg-blue-100 hover:text-blue-600 transition-colors"
        >
          <component :is="action.icon" class="w-4 h-4" />
          {{ action.label }}
        </RouterLink>
      </div>
    </div>

    <!-- 欢迎信息 -->
    <div class="mt-8 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl p-6 text-white">
      <h2 class="text-xl font-semibold mb-2">欢迎使用个人博客管理系统</h2>
      <p class="opacity-90">在这里您可以管理您的文章、评论、分类和标签。</p>
    </div>
  </div>
</template>
