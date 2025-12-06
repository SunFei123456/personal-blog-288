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
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">分类管理</h1>
      <button
        @click="openCreateModal"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        <Plus class="w-4 h-4" />
        新建分类
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- 分类列表 -->
    <div v-else-if="categories.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">ID</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">名称</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">描述</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">文章数</th>
            <th class="text-right px-6 py-4 text-sm font-medium text-gray-500">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="category in categories" :key="category.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-gray-500">{{ category.id }}</td>
            <td class="px-6 py-4 font-medium text-gray-900">{{ category.name }}</td>
            <td class="px-6 py-4 text-gray-500">{{ category.description || '-' }}</td>
            <td class="px-6 py-4 text-gray-500">{{ category.article_count || 0 }}</td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-end gap-2">
                <button
                  @click="openEditModal(category)"
                  class="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                  title="编辑"
                >
                  <Edit class="w-4 h-4" />
                </button>
                <button
                  @click="handleDelete(category)"
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
      <p class="text-gray-500 mb-4">暂无分类</p>
      <button
        @click="openCreateModal"
        class="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        <Plus class="w-4 h-4" />
        创建第一个分类
      </button>
    </div>

    <!-- 新建/编辑弹窗 -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-gray-900">
            {{ editingCategory ? '编辑分类' : '新建分类' }}
          </h2>
          <button @click="closeModal" class="p-2 text-gray-400 hover:text-gray-600">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">分类名称 *</label>
            <input
              v-model="form.name"
              type="text"
              placeholder="请输入分类名称"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">描述</label>
            <textarea
              v-model="form.description"
              placeholder="请输入分类描述（可选）"
              rows="3"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none"
            ></textarea>
          </div>

          <div class="flex justify-end gap-3 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="submitting"
              class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              <Loader2 v-if="submitting" class="w-4 h-4 animate-spin" />
              {{ submitting ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
