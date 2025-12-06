<script setup lang="ts">
/**
 * 评论管理页面
 * - 评论列表
 * - 删除评论
 */

import { ref, onMounted } from 'vue'
import { getAllCommentsApi, deleteCommentApi } from '@/api/comment'
import type { Comment } from '@/types'
import { Trash2, User, Calendar, FileText } from 'lucide-vue-next'

/** 评论列表 */
const comments = ref<Comment[]>([])
const loading = ref(true)

/**
 * 格式化日期
 */
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * 获取评论列表
 */
async function fetchComments() {
  loading.value = true
  try {
    const response = await getAllCommentsApi(1, 100)
    comments.value = response.items
  } catch (error) {
    console.error('获取评论列表失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 删除评论
 */
async function handleDelete(comment: Comment) {
  if (!confirm('确定要删除这条评论吗？')) return

  try {
    await deleteCommentApi(comment.id)
    comments.value = comments.value.filter((c) => c.id !== comment.id)
  } catch (error) {
    console.error('删除评论失败:', error)
    alert('删除失败，请稍后重试')
  }
}

// 初始化
onMounted(fetchComments)
</script>

<template>
  <div>
    <!-- 页面标题 -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">评论管理</h1>
        <p class="text-sm text-gray-500 mt-1">管理用户发表的评论</p>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20 text-gray-400">
      <div class="w-10 h-10 border-4 border-indigo-100 border-t-indigo-500 rounded-full animate-spin mb-4"></div>
      <p class="text-sm">加载中...</p>
    </div>

    <!-- 评论列表 -->
    <div v-else-if="comments.length > 0" class="space-y-4">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="group bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-all"
      >
        <div class="flex items-start justify-between gap-4">
          <div class="flex-1">
            <!-- 评论者信息 -->
            <div class="flex flex-wrap items-center gap-3 text-sm text-gray-500 mb-3">
              <span class="flex items-center gap-1.5 font-medium text-gray-900 bg-gray-50 px-2 py-1 rounded-lg">
                <User class="w-4 h-4 text-indigo-500" />
                {{ comment.user?.username || '匿名用户' }}
              </span>
              <span class="flex items-center gap-1.5 text-xs">
                <Calendar class="w-3.5 h-3.5" />
                {{ formatDate(comment.created_at) }}
              </span>
              <RouterLink 
                :to="`/article/${comment.article_id}`" 
                target="_blank"
                class="flex items-center gap-1.5 text-xs text-indigo-600 hover:text-indigo-700 bg-indigo-50 px-2 py-1 rounded-lg transition-colors"
              >
                <FileText class="w-3.5 h-3.5" />
                查看文章
              </RouterLink>
            </div>

            <!-- 评论内容 -->
            <div class="relative">
              <div class="absolute left-0 top-0 bottom-0 w-1 bg-gray-100 rounded-full"></div>
              <p class="text-gray-700 whitespace-pre-wrap pl-4 leading-relaxed">{{ comment.content }}</p>
            </div>
          </div>

          <!-- 删除按钮 -->
          <button
            @click="handleDelete(comment)"
            class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all opacity-0 group-hover:opacity-100"
            title="删除评论"
          >
            <Trash2 class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="bg-white rounded-2xl shadow-sm border border-gray-100 p-16 text-center">
      <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
        <FileText class="w-8 h-8 text-gray-300" />
      </div>
      <p class="text-gray-500">暂无评论</p>
    </div>
  </div>
</template>
