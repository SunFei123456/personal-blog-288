<script setup lang="ts">
/**
 * 后台管理布局组件
 * - 侧边栏导航
 * - 顶部工具栏
 * - 主内容区域
 */

import { RouterLink, RouterView, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'
import {
  LayoutDashboard,
  FileText,
  MessageSquare,
  FolderOpen,
  Tags,
  Users,
  Home,
  LogOut,
  ChevronRight,
} from 'lucide-vue-next'

const route = useRoute()
const userStore = useUserStore()

/**
 * 侧边栏菜单配置
 */
const menuItems = computed(() => {
  const items = [
    { path: '/admin', name: '控制台', icon: LayoutDashboard },
    { path: '/admin/articles', name: '文章管理', icon: FileText },
    { path: '/admin/comments', name: '评论管理', icon: MessageSquare },
    { path: '/admin/categories', name: '分类管理', icon: FolderOpen },
    { path: '/admin/tags', name: '标签管理', icon: Tags },
  ]

  // 管理员才能看到用户管理
  if (userStore.isAdmin) {
    items.push({ path: '/admin/users', name: '用户管理', icon: Users })
  }

  return items
})

/**
 * 判断菜单是否激活
 */
function isActive(path: string): boolean {
  if (path === '/admin') {
    return route.path === '/admin'
  }
  return route.path.startsWith(path)
}

/**
 * 处理登出
 */
function handleLogout() {
  userStore.logout()
}
</script>

<template>
  <div class="min-h-screen flex bg-gray-100">
    <!-- 侧边栏 -->
    <aside class="w-64 bg-gray-900 text-white flex flex-col">
      <!-- Logo -->
      <div class="h-16 flex items-center justify-center border-b border-gray-800">
        <RouterLink to="/admin" class="text-xl font-bold">
          博客管理后台
        </RouterLink>
      </div>

      <!-- 菜单列表 -->
      <nav class="flex-1 py-4">
        <RouterLink
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-6 py-3 text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
          :class="{ 'bg-gray-800 text-white border-r-4 border-blue-500': isActive(item.path) }"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span>{{ item.name }}</span>
        </RouterLink>
      </nav>

      <!-- 底部链接 -->
      <div class="border-t border-gray-800 py-4">
        <RouterLink
          to="/"
          class="flex items-center gap-3 px-6 py-3 text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
        >
          <Home class="w-5 h-5" />
          <span>返回前台</span>
        </RouterLink>
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-3 px-6 py-3 text-gray-300 hover:bg-gray-800 hover:text-red-400 transition-colors"
        >
          <LogOut class="w-5 h-5" />
          <span>退出登录</span>
        </button>
      </div>
    </aside>

    <!-- 主内容区域 -->
    <div class="flex-1 flex flex-col">
      <!-- 顶部工具栏 -->
      <header class="h-16 bg-white shadow-sm flex items-center justify-between px-6">
        <!-- 面包屑 -->
        <div class="flex items-center gap-2 text-gray-600">
          <RouterLink to="/admin" class="hover:text-blue-600">后台管理</RouterLink>
          <ChevronRight class="w-4 h-4" />
          <span class="text-gray-900">{{ route.meta.title }}</span>
        </div>

        <!-- 用户信息 -->
        <div class="flex items-center gap-3">
          <span class="text-gray-600">
            欢迎，{{ userStore.username }}
            <span v-if="userStore.isAdmin" class="ml-1 px-2 py-0.5 bg-blue-100 text-blue-600 text-xs rounded">
              管理员
            </span>
          </span>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="flex-1 p-6 overflow-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>
