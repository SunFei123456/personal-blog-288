<script setup lang="ts">
/**
 * 文章管理页面
 * - 文章列表
 * - 文章删除
 * - 状态筛选
 */

import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { getMyArticlesApi, getArticlesApi, deleteArticleApi } from '@/api/article'
import { useUserStore } from '@/stores/user'
import type { Article, ArticleStatus } from '@/types'
import { Plus, Edit, Trash2, Eye, Calendar, Filter, FileText } from 'lucide-vue-next'

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
    
    // 管理员获取所有文章，普通用户只获取自己的文章
    const response = userStore.isAdmin 
      ? await getArticlesApi(params)
      : await getMyArticlesApi(params)
    
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
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">文章管理</h1>
        <p class="text-sm text-gray-500 mt-1">管理和发布你的博客文章</p>
      </div>
      <RouterLink
        to="/admin/articles/edit"
        class="flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-200 font-medium"
      >
        <Plus class="w-4 h-4" />
        写文章
      </RouterLink>
    </div>

    <!-- 筛选栏 -->
    <div class="bg-white rounded-2xl p-2 mb-6 shadow-sm border border-gray-100 flex items-center justify-between">
      <div class="flex items-center gap-2 p-1 bg-gray-50/80 rounded-xl">
        <button
          @click="() => { filterStatus = ''; fetchArticles() }"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
          :class="!filterStatus ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'"
        >
          全部
        </button>
        <button
          @click="() => { filterStatus = 'published'; fetchArticles() }"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
          :class="filterStatus === 'published' ? 'bg-white text-green-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'"
        >
          已发布
        </button>
        <button
          @click="() => { filterStatus = 'draft'; fetchArticles() }"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
          :class="filterStatus === 'draft' ? 'bg-white text-orange-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'"
        >
          草稿箱
        </button>
      </div>
      
      <div class="px-4 text-sm text-gray-400">
        共 {{ filteredArticles.length }} 篇文章
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20 text-gray-400">
      <div class="w-10 h-10 border-4 border-indigo-100 border-t-indigo-500 rounded-full animate-spin mb-4"></div>
      <p class="text-sm">加载中...</p>
    </div>

    <!-- 文章列表 -->
    <div v-else-if="filteredArticles.length > 0" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50/50">
          <tr>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">标题</th>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">状态</th>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">数据</th>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">创建时间</th>
            <th class="text-right px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr v-for="article in filteredArticles" :key="article.id" class="group hover:bg-gray-50/80 transition-colors">
            <td class="px-6 py-4">
              <div class="flex flex-col">
                <RouterLink
                  :to="`/article/${article.id}`"
                  class="text-gray-900 font-medium hover:text-indigo-600 transition-colors line-clamp-1"
                  target="_blank"
                >
                  {{ article.title }}
                </RouterLink>
                <span class="text-xs text-gray-400 mt-1 line-clamp-1">{{ article.summary || '暂无摘要' }}</span>
              </div>
            </td>
            <td class="px-6 py-4">
              <span
                class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border"
                :class="{
                  'bg-green-50 text-green-700 border-green-100': article.status === 'published',
                  'bg-orange-50 text-orange-700 border-orange-100': article.status === 'draft',
                }"
              >
                <span class="w-1.5 h-1.5 rounded-full" :class="article.status === 'published' ? 'bg-green-500' : 'bg-orange-500'"></span>
                {{ article.status === 'published' ? '已发布' : '草稿' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-4 text-gray-400 text-sm">
                <span class="flex items-center gap-1.5" title="浏览量">
                  <Eye class="w-4 h-4" />
                  {{ article.view_count }}
                </span>
              </div>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">
              {{ formatDate(article.created_at) }}
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <RouterLink
                  :to="`/admin/articles/edit/${article.id}`"
                  class="p-2 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-all"
                  title="编辑"
                >
                  <Edit class="w-4 h-4" />
                </RouterLink>
                <button
                  @click="handleDelete(article)"
                  class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
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
    <div v-else class="bg-white rounded-2xl shadow-sm border border-gray-100 p-16 text-center">
      <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
        <FileText class="w-8 h-8 text-gray-300" />
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-1">暂无文章</h3>
      <p class="text-gray-500 mb-6">开始创作你的第一篇博客文章吧</p>
      <RouterLink
        to="/admin/articles/edit"
        class="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-colors font-medium shadow-sm"
      >
        <Plus class="w-4 h-4" />
        写第一篇文章
      </RouterLink>
    </div>
  </div>
</template>
