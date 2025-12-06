<script setup lang="ts">
/**
 * 文章详情页
 * - 文章内容展示（Markdown渲染）
 */

import { ref, onMounted, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'
import { getArticleApi } from '@/api/article'
import type { Article } from '@/types'
import { Calendar, Eye, FolderOpen, Tag, ArrowLeft } from 'lucide-vue-next'

const route = useRoute()

/** 文章数据 */
const article = ref<Article | null>(null)
const loading = ref(true)

/** 文章ID */
const articleId = computed(() => parseInt(route.params.id as string))

/**
 * 格式化日期
 */
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * 获取文章详情
 */
async function fetchArticle() {
  loading.value = true
  try {
    article.value = await getArticleApi(articleId.value)
  } catch (error) {
    console.error('获取文章详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 初始化
onMounted(() => {
  fetchArticle()
})
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
      <p class="mt-4 text-gray-500">加载中...</p>
    </div>

    <!-- 文章内容 -->
    <article v-else-if="article" class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <!-- 文章头部 -->
      <header class="p-8 border-b border-gray-100">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ article.title }}</h1>

        <!-- 文章元信息 -->
        <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500">
          <span v-if="article.author" class="flex items-center gap-1">
            <User class="w-4 h-4" />
            {{ article.author.username }}
          </span>
          <span class="flex items-center gap-1">
            <Calendar class="w-4 h-4" />
            {{ formatDate(article.created_at) }}
          </span>
          <span class="flex items-center gap-1">
            <Eye class="w-4 h-4" />
            {{ article.view_count }} 阅读
          </span>
          <span v-if="article.category" class="flex items-center gap-1">
            <FolderOpen class="w-4 h-4" />
            {{ article.category.name }}
          </span>
        </div>

        <!-- 标签 -->
        <div v-if="article.tags && article.tags.length > 0" class="flex items-center gap-2 mt-4">
          <Tag class="w-4 h-4 text-gray-400" />
          <span
            v-for="tag in article.tags"
            :key="tag.id"
            class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
          >
            {{ tag.name }}
          </span>
        </div>
      </header>

      <!-- 文章正文 -->
      <div class="p-8">
        <MdPreview :modelValue="article.content" />
      </div>
    </article>

    <!-- 文章不存在 -->
    <div v-else class="text-center py-12">
      <p class="text-gray-500">文章不存在或已被删除</p>
    </div>
  </div>
</template>
