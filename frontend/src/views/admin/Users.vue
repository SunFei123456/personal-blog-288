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
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">用户管理</h1>
        <p class="text-sm text-gray-500 mt-1">管理注册用户和权限</p>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20 text-gray-400">
      <div class="w-10 h-10 border-4 border-indigo-100 border-t-indigo-500 rounded-full animate-spin mb-4"></div>
      <p class="text-sm">加载中...</p>
    </div>

    <!-- 用户列表 -->
    <div v-else-if="users.length > 0" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50/50">
          <tr>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">用户</th>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">邮箱</th>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">角色</th>
            <th class="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">注册时间</th>
            <th class="text-right px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr v-for="user in users" :key="user.id" class="group hover:bg-gray-50/80 transition-colors">
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center text-indigo-600 font-bold text-xs border-2 border-white shadow-sm">
                  {{ user.username.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <div class="font-medium text-gray-900 flex items-center gap-2">
                    {{ user.username }}
                    <span v-if="user.id === userStore.user?.id" class="px-1.5 py-0.5 rounded text-[10px] bg-indigo-50 text-indigo-600 font-medium border border-indigo-100">YOU</span>
                  </div>
                  <div class="text-xs text-gray-400">ID: {{ user.id }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 text-gray-500">
              <span class="flex items-center gap-1.5 text-sm">
                <Mail class="w-3.5 h-3.5 text-gray-400" />
                {{ user.email }}
              </span>
            </td>
            <td class="px-6 py-4">
              <span
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border"
                :class="{
                  'bg-indigo-50 text-indigo-700 border-indigo-100': user.role === 'admin',
                  'bg-gray-50 text-gray-600 border-gray-100': user.role === 'user',
                }"
              >
                {{ user.role === 'admin' ? '管理员' : '普通用户' }}
              </span>
            </td>
            <td class="px-6 py-4 text-gray-500">
              <span class="flex items-center gap-1.5 text-sm">
                <Calendar class="w-3.5 h-3.5 text-gray-400" />
                {{ formatDate(user.created_at) }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  @click="toggleRole(user)"
                  :disabled="user.id === userStore.user?.id"
                  class="p-2 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  :title="user.role === 'admin' ? '取消管理员' : '设为管理员'"
                >
                  <Shield v-if="user.role === 'user'" class="w-4 h-4" />
                  <ShieldOff v-else class="w-4 h-4" />
                </button>
                <button
                  @click="handleDelete(user)"
                  :disabled="user.id === userStore.user?.id"
                  class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
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
    <div v-else class="bg-white rounded-2xl shadow-sm border border-gray-100 p-16 text-center">
      <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
        <Shield class="w-8 h-8 text-gray-300" />
      </div>
      <p class="text-gray-500">暂无用户</p>
    </div>
  </div>
</template>
