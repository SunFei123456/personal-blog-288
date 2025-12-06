<script setup lang="ts">
/**
 * 标签文章列表页
 * - 按标签筛选文章
 */

import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { getArticlesApi } from '@/api/article'
import type { Article } from '@/types'
import { Calendar, Eye, ArrowLeft, Tag } from 'lucide-vue-next'

const route = useRoute()

/** 文章列表 */
const articles = ref<Article[]>([])
const loading = ref(true)

/** 标签ID */
const tagId = computed(() => parseInt(route.params.id as string))

/**
 * 格式化日期
 */
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

/**
 * 获取标签下的文章列表
 */
async function fetchArticles() {
  loading.value = true
  try {
    const response = await getArticlesApi({
      tag_id: tagId.value,
      status: 'published',
      page_size: 50,
    })
    articles.value = response.items
  } catch (error) {
    console.error('获取文章列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 监听路由变化
watch(() => route.params.id, fetchArticles)

// 初始化
onMounted(fetchArticles)
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- 返回按钮 -->
    <RouterLink to="/" class="inline-flex items-center gap-1 text-gray-600 hover:text-blue-600 mb-6">
      <ArrowLeft class="w-4 h-4" />
      返回首页
    </RouterLink>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- 标签标题 -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 flex items-center gap-3">
          <Tag class="w-8 h-8 text-blue-600" />
          标签文章
        </h1>
        <p class="mt-2 text-gray-500">共 {{ articles.length }} 篇文章</p>
      </div>

      <!-- 文章列表 -->
      <div v-if="articles.length > 0" class="space-y-4">
        <RouterLink
          v-for="article in articles"
          :key="article.id"
          :to="`/article/${article.id}`"
          class="block bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow"
        >
          <h2 class="text-xl font-semibold text-gray-900 hover:text-blue-600 mb-2">
            {{ article.title }}
          </h2>
          <p class="text-gray-600 line-clamp-2 mb-3">
            {{ article.summary || article.content.slice(0, 150) + '...' }}
          </p>
          <div class="flex items-center gap-4 text-sm text-gray-500">
            <span class="flex items-center gap-1">
              <Calendar class="w-4 h-4" />
              {{ formatDate(article.created_at) }}
            </span>
            <span class="flex items-center gap-1">
              <Eye class="w-4 h-4" />
              {{ article.view_count }} 阅读
            </span>
          </div>
        </RouterLink>
      </div>

      <!-- 空状态 -->
      <div v-else class="text-center py-12 text-gray-500">
        该标签下暂无文章
      </div>
    </template>
  </div>
</template>
