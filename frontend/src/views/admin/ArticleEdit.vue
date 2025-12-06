<script setup lang="ts">
/**
 * 文章编辑页面
 * - 新建/编辑文章
 * - Markdown 编辑器
 * - 分类/标签选择
 */

import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { getArticleApi, createArticleApi, updateArticleApi } from '@/api/article'
import { getCategoriesApi } from '@/api/category'
import { getTagsApi } from '@/api/tag'
import type { Category, Tag, ArticleStatus } from '@/types'
import { Save, ArrowLeft, Loader2 } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

/** 文章ID（编辑模式） */
const articleId = computed(() => route.params.id ? parseInt(route.params.id as string) : null)

/** 是否编辑模式 */
const isEditMode = computed(() => !!articleId.value)

/** 表单数据 */
const form = reactive({
  title: '',
  content: '',
  summary: '',
  cover_image: '',
  status: 'draft' as ArticleStatus,
  category_id: null as number | null,
  tag_ids: [] as number[],
})

/** 分类和标签列表 */
const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])

/** 加载状态 */
const loading = ref(false)
const submitting = ref(false)

/**
 * 获取文章详情（编辑模式）
 */
async function fetchArticle() {
  if (!articleId.value) return

  loading.value = true
  try {
    const article = await getArticleApi(articleId.value)
    form.title = article.title
    form.content = article.content
    form.summary = article.summary || ''
    form.cover_image = article.cover_image || ''
    form.status = article.status
    form.category_id = article.category_id || null
    form.tag_ids = article.tags?.map((t) => t.id) || []
  } catch (error) {
    console.error('获取文章详情失败:', error)
    alert('文章不存在或无权限编辑')
    router.push('/admin/articles')
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
 * 提交表单
 */
async function handleSubmit() {
  // 表单验证
  if (!form.title.trim()) {
    alert('请输入文章标题')
    return
  }
  if (!form.content.trim()) {
    alert('请输入文章内容')
    return
  }

  submitting.value = true
  try {
    const data = {
      title: form.title,
      content: form.content,
      summary: form.summary || undefined,
      cover_image: form.cover_image || undefined,
      status: form.status,
      category_id: form.category_id || undefined,
      tag_ids: form.tag_ids.length > 0 ? form.tag_ids : undefined,
    }

    if (isEditMode.value) {
      await updateArticleApi(articleId.value!, data)
      alert('文章更新成功')
    } else {
      await createArticleApi(data)
      alert('文章创建成功')
    }

    router.push('/admin/articles')
  } catch (error: any) {
    console.error('保存文章失败:', error)
    alert(error.response?.data?.detail || '保存失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

/**
 * 切换标签选择
 */
function toggleTag(tagId: number) {
  const index = form.tag_ids.indexOf(tagId)
  if (index > -1) {
    form.tag_ids.splice(index, 1)
  } else {
    form.tag_ids.push(tagId)
  }
}

// 初始化
onMounted(() => {
  fetchCategories()
  fetchTags()
  if (isEditMode.value) {
    fetchArticle()
  }
})
</script>

<template>
  <div>
    <!-- 页面头部 -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-4">
        <button
          @click="router.back()"
          class="p-2 text-gray-400 hover:text-gray-600 transition-colors"
        >
          <ArrowLeft class="w-5 h-5" />
        </button>
        <h1 class="text-2xl font-bold text-gray-900">
          {{ isEditMode ? '编辑文章' : '写文章' }}
        </h1>
      </div>
      <button
        @click="handleSubmit"
        :disabled="submitting"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
      >
        <Loader2 v-if="submitting" class="w-4 h-4 animate-spin" />
        <Save v-else class="w-4 h-4" />
        {{ submitting ? '保存中...' : '保存' }}
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- 编辑表单 -->
    <div v-else class="space-y-6">
      <!-- 基本信息 -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div class="space-y-4">
          <!-- 标题 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">文章标题 *</label>
            <input
              v-model="form.title"
              type="text"
              placeholder="请输入文章标题"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>

          <!-- 摘要 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">文章摘要</label>
            <textarea
              v-model="form.summary"
              placeholder="请输入文章摘要（可选，不填则自动截取内容前150字）"
              rows="2"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none"
            ></textarea>
          </div>

          <!-- 分类和状态 -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">分类</label>
              <select
                v-model="form.category_id"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              >
                <option :value="null">请选择分类</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
              <select
                v-model="form.status"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              >
                <option value="draft">草稿</option>
                <option value="published">发布</option>
              </select>
            </div>
          </div>

          <!-- 标签 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">标签</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="tag in tags"
                :key="tag.id"
                type="button"
                @click="toggleTag(tag.id)"
                class="px-3 py-1 rounded-full text-sm transition-colors"
                :class="form.tag_ids.includes(tag.id)
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
              >
                {{ tag.name }}
              </button>
              <span v-if="tags.length === 0" class="text-gray-400 text-sm">暂无标签</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Markdown 编辑器 -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <MdEditor
          v-model="form.content"
          :preview="true"
          style="height: 600px"
          placeholder="请输入文章内容（支持 Markdown 格式）"
        />
      </div>
    </div>
  </div>
</template>
