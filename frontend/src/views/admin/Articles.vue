<script setup lang="ts">
/**
 * 文章管理页面
 * - 文章列表
 * - 文章删除
 * - 状态筛选
 */

import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { getMyArticlesApi, deleteArticleApi } from '@/api/article'
import { useUserStore } from '@/stores/user'
import type { Article, ArticleStatus } from '@/types'
import { Plus, Edit, Trash2, Eye, Calendar, Filter } from 'lucide-vue-next'

const userStore = useUserStore()

/** 文章列表 */
const articles = ref<Article[]>([])
const loading = ref(true)

/** 筛选状态 */
const filterStatus = ref<ArticleStatus | ''>('')

/**
 * 格式化日期
 */
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

/**
 * 获取文章列表
 */
async function fetchArticles() {
  loading.value = true
  try {
    const params: any = { page_size: 100 }
    if (filterStatus.value) {
      params.status = filterStatus.value
    }
    const response = await getMyArticlesApi(params)
    articles.value = response.items
  } catch (error) {
    console.error('获取文章列表失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 删除文章
 */
async function handleDelete(article: Article) {
  if (!confirm(`确定要删除文章《${article.title}》吗？`)) return

  try {
    await deleteArticleApi(article.id)
    articles.value = articles.value.filter((a) => a.id !== article.id)
  } catch (error) {
    console.error('删除文章失败:', error)
    alert('删除失败，请稍后重试')
  }
}

/**
 * 筛选后的文章列表
 */
const filteredArticles = computed(() => {
  if (!filterStatus.value) return articles.value
  return articles.value.filter((a) => a.status === filterStatus.value)
})

// 初始化
onMounted(fetchArticles)
</script>

<template>
  <div>
    <!-- 页面头部 -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">文章管理</h1>
      <RouterLink
        to="/admin/articles/edit"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        <Plus class="w-4 h-4" />
        写文章
      </RouterLink>
    </div>

    <!-- 筛选栏 -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6">
      <div class="flex items-center gap-4">
        <Filter class="w-5 h-5 text-gray-400" />
        <select
          v-model="filterStatus"
          @change="fetchArticles"
          class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
        >
          <option value="">全部状态</option>
          <option value="published">已发布</option>
          <option value="draft">草稿</option>
        </select>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- 文章列表 -->
    <div v-else-if="filteredArticles.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">标题</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">状态</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">浏览量</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">创建时间</th>
            <th class="text-right px-6 py-4 text-sm font-medium text-gray-500">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="article in filteredArticles" :key="article.id" class="hover:bg-gray-50">
            <td class="px-6 py-4">
              <RouterLink
                :to="`/article/${article.id}`"
                class="text-gray-900 hover:text-blue-600 font-medium"
                target="_blank"
              >
                {{ article.title }}
              </RouterLink>
            </td>
            <td class="px-6 py-4">
              <span
                class="px-2 py-1 text-xs rounded-full"
                :class="{
                  'bg-green-100 text-green-600': article.status === 'published',
                  'bg-gray-100 text-gray-600': article.status === 'draft',
                }"
              >
                {{ article.status === 'published' ? '已发布' : '草稿' }}
              </span>
            </td>
            <td class="px-6 py-4 text-gray-500">
              <span class="flex items-center gap-1">
                <Eye class="w-4 h-4" />
                {{ article.view_count }}
              </span>
            </td>
            <td class="px-6 py-4 text-gray-500">
              <span class="flex items-center gap-1">
                <Calendar class="w-4 h-4" />
                {{ formatDate(article.created_at) }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-end gap-2">
                <RouterLink
                  :to="`/admin/articles/edit/${article.id}`"
                  class="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                  title="编辑"
                >
                  <Edit class="w-4 h-4" />
                </RouterLink>
                <button
                  @click="handleDelete(article)"
                  class="p-2 text-gray-400 hover:text-red-600 transition-colors"
                  title="删除"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 空状态 -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
      <p class="text-gray-500 mb-4">暂无文章</p>
      <RouterLink
        to="/admin/articles/edit"
        class="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        <Plus class="w-4 h-4" />
        写第一篇文章
      </RouterLink>
    </div>
  </div>
</template>
