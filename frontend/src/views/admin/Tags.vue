<script setup lang="ts">
/**
 * 标签管理页面
 * - 标签列表
 * - 新建/删除标签
 */

import { ref, onMounted } from 'vue'
import { getTagsApi, createTagApi, deleteTagApi } from '@/api/tag'
import type { Tag } from '@/types'
import { Plus, X, Loader2 } from 'lucide-vue-next'

/** 标签列表 */
const tags = ref<Tag[]>([])
const loading = ref(true)

/** 新建标签 */
const newTagName = ref('')
const creating = ref(false)

/**
 * 获取标签列表
 */
async function fetchTags() {
  loading.value = true
  try {
    tags.value = await getTagsApi()
  } catch (error) {
    console.error('获取标签列表失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 创建标签
 */
async function handleCreate() {
  if (!newTagName.value.trim()) {
    alert('请输入标签名称')
    return
  }

  creating.value = true
  try {
    const created = await createTagApi({ name: newTagName.value })
    tags.value.push(created)
    newTagName.value = ''
  } catch (error: any) {
    console.error('创建标签失败:', error)
    alert(error.response?.data?.detail || '创建失败，请稍后重试')
  } finally {
    creating.value = false
  }
}

/**
 * 删除标签
 */
async function handleDelete(tag: Tag) {
  if (!confirm(`确定要删除标签「${tag.name}」吗？`)) return

  try {
    await deleteTagApi(tag.id)
    tags.value = tags.value.filter((t) => t.id !== tag.id)
  } catch (error) {
    console.error('删除标签失败:', error)
    alert('删除失败，请稍后重试')
  }
}

// 初始化
onMounted(fetchTags)
</script>

<template>
  <div>
    <!-- 页面标题 -->
    <h1 class="text-2xl font-bold text-gray-900 mb-6">标签管理</h1>

    <!-- 新建标签 -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">新建标签</h2>
      <form @submit.prevent="handleCreate" class="flex gap-4">
        <input
          v-model="newTagName"
          type="text"
          placeholder="请输入标签名称"
          class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
        />
        <button
          type="submit"
          :disabled="creating"
          class="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          <Loader2 v-if="creating" class="w-4 h-4 animate-spin" />
          <Plus v-else class="w-4 h-4" />
          {{ creating ? '创建中...' : '创建' }}
        </button>
      </form>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- 标签列表 -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">标签列表</h2>
      
      <div v-if="tags.length > 0" class="flex flex-wrap gap-3">
        <div
          v-for="tag in tags"
          :key="tag.id"
          class="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-full group"
        >
          <span class="text-gray-700">{{ tag.name }}</span>
          <span class="text-gray-400 text-sm">({{ tag.article_count || 0 }})</span>
          <button
            @click="handleDelete(tag)"
            class="p-1 text-gray-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-all"
            title="删除标签"
          >
            <X class="w-4 h-4" />
          </button>
        </div>
      </div>

      <p v-else class="text-gray-500 text-center py-8">暂无标签</p>
    </div>
  </div>
</template>
