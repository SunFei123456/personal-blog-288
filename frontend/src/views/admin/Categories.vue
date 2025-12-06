<script setup lang="ts">
/**
 * 分类管理页面
 * - 分类列表
 * - 新建/编辑/删除分类
 */

import { ref, reactive, onMounted } from 'vue'
import { getCategoriesApi, createCategoryApi, updateCategoryApi, deleteCategoryApi } from '@/api/category'
import type { Category } from '@/types'
import { Plus, Edit, Trash2, X, Loader2 } from 'lucide-vue-next'

/** 分类列表 */
const categories = ref<Category[]>([])
const loading = ref(true)

/** 弹窗状态 */
const showModal = ref(false)
const editingCategory = ref<Category | null>(null)
const submitting = ref(false)

/** 表单数据 */
const form = reactive({
  name: '',
  description: '',
})

/**
 * 获取分类列表
 */
async function fetchCategories() {
  loading.value = true
  try {
    categories.value = await getCategoriesApi()
  } catch (error) {
    console.error('获取分类列表失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 打开新建弹窗
 */
function openCreateModal() {
  editingCategory.value = null
  form.name = ''
  form.description = ''
  showModal.value = true
}

/**
 * 打开编辑弹窗
 */
function openEditModal(category: Category) {
  editingCategory.value = category
  form.name = category.name
  form.description = category.description || ''
  showModal.value = true
}

/**
 * 关闭弹窗
 */
function closeModal() {
  showModal.value = false
  editingCategory.value = null
}

/**
 * 提交表单
 */
async function handleSubmit() {
  if (!form.name.trim()) {
    alert('请输入分类名称')
    return
  }

  submitting.value = true
  try {
    if (editingCategory.value) {
      // 更新分类
      const updated = await updateCategoryApi(editingCategory.value.id, {
        name: form.name,
        description: form.description || undefined,
      })
      const index = categories.value.findIndex((c) => c.id === updated.id)
      if (index > -1) {
        categories.value[index] = updated
      }
    } else {
      // 创建分类
      const created = await createCategoryApi({
        name: form.name,
        description: form.description || undefined,
      })
      categories.value.push(created)
    }
    closeModal()
  } catch (error: any) {
    console.error('保存分类失败:', error)
    alert(error.response?.data?.detail || '保存失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

/**
 * 删除分类
 */
async function handleDelete(category: Category) {
  if (!confirm(`确定要删除分类「${category.name}」吗？`)) return

  try {
    await deleteCategoryApi(category.id)
    categories.value = categories.value.filter((c) => c.id !== category.id)
  } catch (error) {
    console.error('删除分类失败:', error)
    alert('删除失败，请稍后重试')
  }
}

// 初始化
onMounted(fetchCategories)
</script>

<template>
  <div>
    <!-- 页面头部 -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">分类管理</h1>
        <p class="text-sm text-gray-500 mt-1">创建和管理文章分类</p>
      </div>
      <button
        @click="openCreateModal"
        class="flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-200 font-medium"
      >
        <Plus class="w-4 h-4" />
        新建分类
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20 text-gray-400">
      <div class="w-10 h-10 border-4 border-indigo-100 border-t-indigo-500 rounded-full animate-spin mb-4"></div>
      <p class="text-sm">加载中...</p>
    </div>

    <!-- 分类列表 -->
    <div v-else-if="categories.length > 0" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50/50">
          <tr>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">名称</th>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">描述</th>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">文章数</th>
            <th class="text-right px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr v-for="category in categories" :key="category.id" class="group hover:bg-gray-50/80 transition-colors">
            <td class="px-6 py-4">
              <span class="font-medium text-gray-900">{{ category.name }}</span>
            </td>
            <td class="px-6 py-4 text-gray-500 text-sm max-w-md truncate">{{ category.description || '-' }}</td>
            <td class="px-6 py-4">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700">
                {{ category.article_count || 0 }} 篇
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  @click="openEditModal(category)"
                  class="p-2 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-all"
                  title="编辑"
                >
                  <Edit class="w-4 h-4" />
                </button>
                <button
                  @click="handleDelete(category)"
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
        <Plus class="w-8 h-8 text-gray-300" />
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-1">暂无分类</h3>
      <p class="text-gray-500 mb-6">创建一个分类来组织你的文章</p>
      <button
        @click="openCreateModal"
        class="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-colors font-medium shadow-sm"
      >
        <Plus class="w-4 h-4" />
        创建第一个分类
      </button>
    </div>

    <!-- 新建/编辑弹窗 -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-gray-900/20 backdrop-blur-sm flex items-center justify-center z-50 transition-all"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8 transform transition-all scale-100">
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-xl font-bold text-gray-900">
            {{ editingCategory ? '编辑分类' : '新建分类' }}
          </h2>
          <button @click="closeModal" class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">分类名称 <span class="text-red-500">*</span></label>
            <input
              v-model="form.name"
              type="text"
              placeholder="例如：技术分享"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">描述</label>
            <textarea
              v-model="form.description"
              placeholder="简单描述一下这个分类..."
              rows="3"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none resize-none transition-all"
            ></textarea>
          </div>

          <div class="flex justify-end gap-3 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="px-5 py-2.5 border border-gray-200 text-gray-600 font-medium rounded-xl hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="submitting"
              class="flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 disabled:opacity-70 disabled:cursor-not-allowed transition-all shadow-lg shadow-indigo-200"
            >
              <Loader2 v-if="submitting" class="w-4 h-4 animate-spin" />
              {{ submitting ? '保存中...' : '保存分类' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
