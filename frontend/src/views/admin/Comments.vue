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
    <h1 class="text-2xl font-bold text-gray-900 mb-6">评论管理</h1>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- 评论列表 -->
    <div v-else-if="comments.length > 0" class="space-y-4">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <!-- 评论者信息 -->
            <div class="flex items-center gap-4 text-sm text-gray-500 mb-3">
              <span class="flex items-center gap-1">
                <User class="w-4 h-4" />
                {{ comment.user?.username || '匿名用户' }}
              </span>
              <span class="flex items-center gap-1">
                <Calendar class="w-4 h-4" />
                {{ formatDate(comment.created_at) }}
              </span>
              <span class="flex items-center gap-1">
                <FileText class="w-4 h-4" />
                文章ID: {{ comment.article_id }}
              </span>
            </div>

            <!-- 评论内容 -->
            <p class="text-gray-700 whitespace-pre-wrap">{{ comment.content }}</p>
          </div>

          <!-- 删除按钮 -->
          <button
            @click="handleDelete(comment)"
            class="p-2 text-gray-400 hover:text-red-600 transition-colors"
            title="删除评论"
          >
            <Trash2 class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
      <p class="text-gray-500">暂无评论</p>
    </div>
  </div>
</template>
