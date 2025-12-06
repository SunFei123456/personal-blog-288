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
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">标签管理</h1>
        <p class="text-sm text-gray-500 mt-1">管理文章标签云</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- 新建标签 -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sticky top-24">
          <h2 class="text-lg font-bold text-gray-900 mb-4">新建标签</h2>
          <form @submit.prevent="handleCreate" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">标签名称</label>
              <input
                v-model="newTagName"
                type="text"
                placeholder="例如：Vue3"
                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
              />
            </div>
            <button
              type="submit"
              :disabled="creating"
              class="w-full flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 disabled:opacity-70 transition-all shadow-lg shadow-indigo-200"
            >
              <Loader2 v-if="creating" class="w-4 h-4 animate-spin" />
              <Plus v-else class="w-4 h-4" />
              {{ creating ? '创建中...' : '创建标签' }}
            </button>
          </form>
        </div>
      </div>

      <!-- 标签列表 -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 min-h-[400px]">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-bold text-gray-900">全部标签</h2>
            <span class="text-sm text-gray-500">共 {{ tags.length }} 个标签</span>
          </div>
          
          <!-- 加载状态 -->
          <div v-if="loading" class="flex flex-col items-center justify-center py-12 text-gray-400">
            <div class="w-8 h-8 border-4 border-indigo-100 border-t-indigo-500 rounded-full animate-spin mb-4"></div>
            <p class="text-sm">加载中...</p>
          </div>

          <div v-else-if="tags.length > 0" class="flex flex-wrap gap-3">
            <div
              v-for="tag in tags"
              :key="tag.id"
              class="group relative flex items-center gap-2 pl-4 pr-2 py-2 bg-gray-50 hover:bg-indigo-50 text-gray-700 hover:text-indigo-700 rounded-xl transition-all border border-transparent hover:border-indigo-100"
            >
              <span class="font-medium">{{ tag.name }}</span>
              <span class="bg-white/50 px-1.5 py-0.5 rounded text-xs text-gray-400 group-hover:text-indigo-500 transition-colors">
                {{ tag.article_count || 0 }}
              </span>
              <button
                @click="handleDelete(tag)"
                class="p-1 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg opacity-0 group-hover:opacity-100 transition-all ml-1"
                title="删除标签"
              >
                <X class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          <div v-else class="flex flex-col items-center justify-center py-16 text-gray-400">
            <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
              <Plus class="w-8 h-8 text-gray-300" />
            </div>
            <p>暂无标签，请在左侧创建</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
