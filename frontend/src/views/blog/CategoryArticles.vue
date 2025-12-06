<script setup lang="ts">
/**
 * 分类文章列表页
 * - 按分类筛选文章
 */

import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { getArticlesApi } from '@/api/article'
import { getCategoryApi } from '@/api/category'
import type { Article, Category } from '@/types'
import { Calendar, Eye, ArrowLeft, FolderOpen } from 'lucide-vue-next'

const route = useRoute()

/** 分类信息 */
const category = ref<Category | null>(null)

/** 文章列表 */
const articles = ref<Article[]>([])
const loading = ref(true)

/** 分类ID */
const categoryId = computed(() => parseInt(route.params.id as string))

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
 * 获取分类信息和文章列表
 */
async function fetchData() {
  loading.value = true
  try {
    // 获取分类信息
    category.value = await getCategoryApi(categoryId.value)
    
    // 获取该分类下的文章
    const response = await getArticlesApi({
      category_id: categoryId.value,
      status: 'published',
      page_size: 50,
    })
    articles.value = response.items
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 监听路由变化
watch(() => route.params.id, fetchData)

// 初始化
onMounted(fetchData)
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
      <!-- 分类标题 -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 flex items-center gap-3">
          <FolderOpen class="w-8 h-8 text-blue-600" />
          {{ category?.name || '分类' }}
        </h1>
        <p v-if="category?.description" class="mt-2 text-gray-600">{{ category.description }}</p>
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
        该分类下暂无文章
      </div>
    </template>
  </div>
</template>
