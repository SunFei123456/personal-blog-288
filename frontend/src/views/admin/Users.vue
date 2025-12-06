<script setup lang="ts">
/**
 * 用户管理页面（管理员专用）
 * - 用户列表
 * - 修改用户角色
 * - 删除用户
 */

import { ref, onMounted } from 'vue'
import { getUsersApi, updateUserApi, deleteUserApi } from '@/api/admin'
import { useUserStore } from '@/stores/user'
import type { User } from '@/types'
import { Trash2, Shield, ShieldOff, Calendar, Mail } from 'lucide-vue-next'

const userStore = useUserStore()

/** 用户列表 */
const users = ref<User[]>([])
const loading = ref(true)

/**
 * 格式化日期
 */
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

/**
 * 获取用户列表
 */
async function fetchUsers() {
  loading.value = true
  try {
    const response = await getUsersApi(1, 100)
    users.value = response.items
  } catch (error) {
    console.error('获取用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 切换用户角色
 */
async function toggleRole(user: User) {
  const newRole = user.role === 'admin' ? 'user' : 'admin'
  const action = newRole === 'admin' ? '设为管理员' : '取消管理员'
  
  if (!confirm(`确定要将用户「${user.username}」${action}吗？`)) return

  try {
    const updated = await updateUserApi(user.id, { role: newRole })
    const index = users.value.findIndex((u) => u.id === user.id)
    if (index > -1) {
      users.value[index] = updated
    }
  } catch (error) {
    console.error('更新用户角色失败:', error)
    alert('操作失败，请稍后重试')
  }
}

/**
 * 删除用户
 */
async function handleDelete(user: User) {
  if (user.id === userStore.user?.id) {
    alert('不能删除自己的账户')
    return
  }

  if (!confirm(`确定要删除用户「${user.username}」吗？此操作不可恢复！`)) return

  try {
    await deleteUserApi(user.id)
    users.value = users.value.filter((u) => u.id !== user.id)
  } catch (error) {
    console.error('删除用户失败:', error)
    alert('删除失败，请稍后重试')
  }
}

// 初始化
onMounted(fetchUsers)
</script>

<template>
  <div>
    <!-- 页面标题 -->
    <h1 class="text-2xl font-bold text-gray-900 mb-6">用户管理</h1>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- 用户列表 -->
    <div v-else-if="users.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">ID</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">用户名</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">邮箱</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">角色</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">注册时间</th>
            <th class="text-right px-6 py-4 text-sm font-medium text-gray-500">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-gray-500">{{ user.id }}</td>
            <td class="px-6 py-4 font-medium text-gray-900">
              {{ user.username }}
              <span v-if="user.id === userStore.user?.id" class="ml-2 text-xs text-blue-600">(我)</span>
            </td>
            <td class="px-6 py-4 text-gray-500">
              <span class="flex items-center gap-1">
                <Mail class="w-4 h-4" />
                {{ user.email }}
              </span>
            </td>
            <td class="px-6 py-4">
              <span
                class="px-2 py-1 text-xs rounded-full"
                :class="{
                  'bg-blue-100 text-blue-600': user.role === 'admin',
                  'bg-gray-100 text-gray-600': user.role === 'user',
                }"
              >
                {{ user.role === 'admin' ? '管理员' : '普通用户' }}
              </span>
            </td>
            <td class="px-6 py-4 text-gray-500">
              <span class="flex items-center gap-1">
                <Calendar class="w-4 h-4" />
                {{ formatDate(user.created_at) }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-end gap-2">
                <button
                  @click="toggleRole(user)"
                  :disabled="user.id === userStore.user?.id"
                  class="p-2 text-gray-400 hover:text-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  :title="user.role === 'admin' ? '取消管理员' : '设为管理员'"
                >
                  <Shield v-if="user.role === 'user'" class="w-4 h-4" />
                  <ShieldOff v-else class="w-4 h-4" />
                </button>
                <button
                  @click="handleDelete(user)"
                  :disabled="user.id === userStore.user?.id"
                  class="p-2 text-gray-400 hover:text-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  title="删除用户"
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
      <p class="text-gray-500">暂无用户</p>
    </div>
  </div>
</template>
