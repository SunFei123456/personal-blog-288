<script setup lang="ts">
/**
 * 文章详情页
 * - 文章内容展示（Markdown渲染）
 * - 评论列表
 * - 评论功能
 */

import { ref, onMounted, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'
import { getArticleApi } from '@/api/article'
import { getCommentsApi, createCommentApi, deleteCommentApi } from '@/api/comment'
import { useUserStore } from '@/stores/user'
import type { Article, Comment } from '@/types'
import { Calendar, Eye, FolderOpen, Tag, User, Send, Trash2, ArrowLeft } from 'lucide-vue-next'

const route = useRoute()
const userStore = useUserStore()

/** 文章数据 */
const article = ref<Article | null>(null)
const loading = ref(true)

/** 评论数据 */
const comments = ref<Comment[]>([])
const commentContent = ref('')
const submittingComment = ref(false)

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

/**
 * 获取评论列表
 */
async function fetchComments() {
  try {
    const response = await getCommentsApi(articleId.value)
    comments.value = response.items
  } catch (error) {
    console.error('获取评论列表失败:', error)
  }
}

/**
 * 提交评论
 */
async function submitComment() {
  if (!commentContent.value.trim()) return
  if (!userStore.isLoggedIn) {
    alert('请先登录后再评论')
    return
  }

  submittingComment.value = true
  try {
    const newComment = await createCommentApi(articleId.value, {
      content: commentContent.value,
    })
    comments.value.unshift(newComment)
    commentContent.value = ''
  } catch (error) {
    console.error('提交评论失败:', error)
    alert('评论失败，请稍后重试')
  } finally {
    submittingComment.value = false
  }
}

/**
 * 删除评论
 */
async function handleDeleteComment(commentId: number) {
  if (!confirm('确定要删除这条评论吗？')) return

  try {
    await deleteCommentApi(commentId)
    comments.value = comments.value.filter((c) => c.id !== commentId)
  } catch (error) {
    console.error('删除评论失败:', error)
    alert('删除失败，请稍后重试')
  }
}

/**
 * 判断是否可以删除评论
 */
function canDeleteComment(comment: Comment): boolean {
  if (!userStore.user) return false
  // 管理员或评论作者可以删除
  return userStore.isAdmin || comment.user_id === userStore.user.id
}

// 初始化
onMounted(() => {
  fetchArticle()
  fetchComments()
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

    <!-- 评论区 -->
    <section v-if="article" class="mt-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">评论 ({{ comments.length }})</h2>

      <!-- 评论输入框 -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
        <textarea
          v-model="commentContent"
          placeholder="写下你的评论..."
          rows="3"
          class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none"
          :disabled="!userStore.isLoggedIn"
        ></textarea>
        <div class="flex items-center justify-between mt-4">
          <p v-if="!userStore.isLoggedIn" class="text-sm text-gray-500">
            请先 <RouterLink to="/login" class="text-blue-600">登录</RouterLink> 后再评论
          </p>
          <span v-else></span>
          <button
            @click="submitComment"
            :disabled="!commentContent.trim() || submittingComment || !userStore.isLoggedIn"
            class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send class="w-4 h-4" />
            {{ submittingComment ? '提交中...' : '发表评论' }}
          </button>
        </div>
      </div>

      <!-- 评论列表 -->
      <div class="space-y-4">
        <div
          v-for="comment in comments"
          :key="comment.id"
          class="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
        >
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <User class="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ comment.user?.username || '匿名用户' }}</p>
                <p class="text-sm text-gray-500">{{ formatDate(comment.created_at) }}</p>
              </div>
            </div>
            <button
              v-if="canDeleteComment(comment)"
              @click="handleDeleteComment(comment.id)"
              class="p-2 text-gray-400 hover:text-red-600 transition-colors"
              title="删除评论"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
          <p class="mt-4 text-gray-700 whitespace-pre-wrap">{{ comment.content }}</p>
        </div>

        <!-- 空评论状态 -->
        <div v-if="comments.length === 0" class="text-center py-8 text-gray-500">
          暂无评论，快来抢沙发吧！
        </div>
      </div>
    </section>
  </div>
</template>
