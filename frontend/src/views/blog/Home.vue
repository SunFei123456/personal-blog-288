<script setup lang="ts">
/**
 * 博客首页
 * - 文章列表展示
 * - 分类/标签筛选
 * - 分页功能
 */

import { ref, onMounted, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { getArticlesApi } from '@/api/article'
import { getCategoriesApi } from '@/api/category'
import { getTagsApi } from '@/api/tag'
import type { Article, Category, Tag, PaginatedResponse } from '@/types'
import { Calendar, Eye, FolderOpen, Tag as TagIcon, ChevronLeft, ChevronRight } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

/** 文章列表数据 */
const articles = ref<Article[]>([])
const totalPages = ref(0)
const currentPage = ref(1)
const loading = ref(false)

/** 分类和标签 */
const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])

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
 * 获取文章列表
 */
async function fetchArticles() {
  loading.value = true
  try {
    const response = await getArticlesApi({
      page: currentPage.value,
      page_size: 10,
      status: 'published',
    })
    articles.value = response.items
    totalPages.value = response.total_pages
  } catch (error) {
    console.error('获取文章列表失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 获取分类列表
 */
async function fetchCategories() {
  try {
    categories.value = await getCategoriesApi()
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

/**
 * 获取标签列表
 */
async function fetchTags() {
  try {
    tags.value = await getTagsApi()
  } catch (error) {
    console.error('获取标签列表失败:', error)
  }
}

/**
 * 切换页码
 */
function changePage(page: number) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  router.push({ query: { ...route.query, page: page.toString() } })
}

// 监听路由变化
watch(
  () => route.query.page,
  (newPage) => {
    currentPage.value = parseInt(newPage as string) || 1
    fetchArticles()
  }
)

// 初始化
onMounted(() => {
  currentPage.value = parseInt(route.query.page as string) || 1
  fetchArticles()
  fetchCategories()
  fetchTags()
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <div class="flex gap-8">
      <!-- 主内容区 -->
      <div class="flex-1">
        <!-- 页面标题 -->
        <h1 class="text-3xl font-bold text-gray-900 mb-8">最新文章</h1>

        <!-- 加载状态 -->
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p class="mt-4 text-gray-500">加载中...</p>
        </div>

        <!-- 文章列表 -->
        <div v-else-if="articles.length > 0" class="space-y-6">
          <article
            v-for="article in articles"
            :key="article.id"
            class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
          >
            <RouterLink :to="`/article/${article.id}`" class="block p-6">
              <!-- 文章标题 -->
              <h2 class="text-xl font-semibold text-gray-900 hover:text-blue-600 transition-colors mb-3">
                {{ article.title }}
              </h2>

              <!-- 文章摘要 -->
              <p class="text-gray-600 line-clamp-2 mb-4">
                {{ article.summary || article.content.slice(0, 150) + '...' }}
              </p>

              <!-- 文章元信息 -->
              <div class="flex items-center gap-4 text-sm text-gray-500">
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
              <div v-if="article.tags && article.tags.length > 0" class="flex items-center gap-2 mt-3">
                <TagIcon class="w-4 h-4 text-gray-400" />
                <span
                  v-for="tag in article.tags"
                  :key="tag.id"
                  class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
                >
                  {{ tag.name }}
                </span>
              </div>
            </RouterLink>
          </article>
        </div>

        <!-- 空状态 -->
        <div v-else class="text-center py-12">
          <p class="text-gray-500">暂无文章</p>
        </div>

        <!-- 分页 -->
        <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-8">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage <= 1"
            class="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft class="w-5 h-5" />
          </button>

          <span class="px-4 py-2 text-gray-600">
            第 {{ currentPage }} / {{ totalPages }} 页
          </span>

          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage >= totalPages"
            class="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronRight class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- 侧边栏 -->
      <aside class="w-72 flex-shrink-0">
        <!-- 分类 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <FolderOpen class="w-5 h-5" />
            分类
          </h3>
          <div class="space-y-2">
            <RouterLink
              v-for="category in categories"
              :key="category.id"
              :to="`/category/${category.id}`"
              class="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-gray-50 text-gray-600 hover:text-blue-600 transition-colors"
            >
              <span>{{ category.name }}</span>
              <span class="text-sm text-gray-400">{{ category.article_count || 0 }}</span>
            </RouterLink>
            <p v-if="categories.length === 0" class="text-gray-400 text-sm">暂无分类</p>
          </div>
        </div>

        <!-- 标签 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TagIcon class="w-5 h-5" />
            标签
          </h3>
          <div class="flex flex-wrap gap-2">
            <RouterLink
              v-for="tag in tags"
              :key="tag.id"
              :to="`/tag/${tag.id}`"
              class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm hover:bg-blue-100 hover:text-blue-600 transition-colors"
            >
              {{ tag.name }}
            </RouterLink>
            <p v-if="tags.length === 0" class="text-gray-400 text-sm">暂无标签</p>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>
