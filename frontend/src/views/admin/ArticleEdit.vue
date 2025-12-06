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
import { Save, ArrowLeft, Loader2, Settings } from 'lucide-vue-next'

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
    <div class="flex items-center justify-between mb-8 sticky top-20 z-30 bg-gray-50/95 backdrop-blur py-2 transition-all">
      <div class="flex items-center gap-4">
        <button
          @click="router.back()"
          class="p-2.5 bg-white text-gray-400 hover:text-gray-600 border border-gray-200 rounded-xl hover:shadow-sm transition-all"
        >
          <ArrowLeft class="w-5 h-5" />
        </button>
        <div>
          <h1 class="text-2xl font-bold text-gray-900 tracking-tight">
            {{ isEditMode ? '编辑文章' : '写文章' }}
          </h1>
          <p class="text-sm text-gray-500 mt-1">
            {{ isEditMode ? '更新您的精彩内容' : '开始创作新的篇章' }}
          </p>
        </div>
      </div>
      <button
        @click="handleSubmit"
        :disabled="submitting"
        class="flex items-center gap-2 px-6 py-2.5 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 disabled:opacity-70 transition-all shadow-lg shadow-indigo-200"
      >
        <Loader2 v-if="submitting" class="w-4 h-4 animate-spin" />
        <Save v-else class="w-4 h-4" />
        {{ submitting ? '保存中...' : '保存文章' }}
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20 text-gray-400">
      <div class="w-10 h-10 border-4 border-indigo-100 border-t-indigo-500 rounded-full animate-spin mb-4"></div>
      <p class="text-sm">加载中...</p>
    </div>

    <!-- 编辑表单 -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- 左侧：主要内容 -->
      <div class="lg:col-span-2 space-y-6">
        <!-- 标题输入 -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <label class="block text-sm font-bold text-gray-700 mb-2">文章标题 <span class="text-red-500">*</span></label>
          <input
            v-model="form.title"
            type="text"
            placeholder="请输入精彩的标题..."
            class="w-full px-5 py-4 text-lg font-medium border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all placeholder:font-normal"
          />
        </div>

        <!-- Markdown 编辑器 -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <MdEditor
            v-model="form.content"
            :preview="true"
            style="height: 700px"
            placeholder="在此处开始您的创作（支持 Markdown 格式）..."
          />
        </div>
      </div>

      <!-- 右侧：设置栏 -->
      <div class="lg:col-span-1 space-y-6">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sticky top-36">
          <h3 class="text-lg font-bold text-gray-900 mb-6 flex items-center gap-2">
            <Settings class="w-5 h-5 text-indigo-600" />
            发布设置
          </h3>
          
          <div class="space-y-6">
            <!-- 摘要 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">摘要</label>
              <textarea
                v-model="form.summary"
                placeholder="文章的简短介绍..."
                rows="4"
                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none resize-none transition-all text-sm"
              ></textarea>
            </div>

            <!-- 分类 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">分类</label>
              <div class="relative">
                <select
                  v-model="form.category_id"
                  class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none appearance-none transition-all"
                >
                  <option :value="null">请选择分类</option>
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
                <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                </div>
              </div>
            </div>

            <!-- 状态 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">状态</label>
              <div class="grid grid-cols-2 gap-3 bg-gray-50 p-1 rounded-xl border border-gray-200">
                <button
                  type="button"
                  @click="form.status = 'draft'"
                  class="py-2 px-4 rounded-lg text-sm font-medium transition-all"
                  :class="form.status === 'draft' ? 'bg-white text-orange-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'"
                >
                  草稿
                </button>
                <button
                  type="button"
                  @click="form.status = 'published'"
                  class="py-2 px-4 rounded-lg text-sm font-medium transition-all"
                  :class="form.status === 'published' ? 'bg-white text-green-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'"
                >
                  发布
                </button>
              </div>
            </div>

            <!-- 标签 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">标签</label>
              <div class="flex flex-wrap gap-2 min-h-[40px]">
                <button
                  v-for="tag in tags"
                  :key="tag.id"
                  type="button"
                  @click="toggleTag(tag.id)"
                  class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all border"
                  :class="form.tag_ids.includes(tag.id)
                    ? 'bg-indigo-50 text-indigo-600 border-indigo-200'
                    : 'bg-white text-gray-600 border-gray-200 hover:border-gray-300 hover:bg-gray-50'"
                >
                  {{ tag.name }}
                </button>
                <span v-if="tags.length === 0" class="text-gray-400 text-sm py-2">暂无标签，请先去创建</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
