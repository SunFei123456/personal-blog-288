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
  <div class="min-h-screen flex bg-gray-50/50">
    <!-- 侧边栏 -->
    <aside class="w-64 bg-white border-r border-gray-100 flex flex-col fixed inset-y-0 left-0 z-50">
      <!-- Logo -->
      <div class="h-16 flex items-center px-8 border-b border-gray-50">
        <RouterLink to="/admin" class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
            <LayoutDashboard class="w-5 h-5" />
          </div>
          <span class="text-lg font-bold text-gray-900 tracking-tight">Blog Admin</span>
        </RouterLink>
      </div>

      <!-- 菜单列表 -->
      <nav class="flex-1 px-4 py-6 space-y-1">
        <div class="px-4 mb-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">
          Menu
        </div>
        <RouterLink
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group relative"
          :class="[
            isActive(item.path)
              ? 'bg-indigo-50 text-indigo-600 font-medium shadow-sm shadow-indigo-100'
              : 'text-gray-500 hover:bg-gray-50 hover:text-gray-900'
          ]"
        >
          <component 
            :is="item.icon" 
            class="w-5 h-5 transition-colors"
            :class="isActive(item.path) ? 'text-indigo-600' : 'text-gray-400 group-hover:text-gray-600'" 
          />
          <span>{{ item.name }}</span>
          
          <!-- 激活指示器 -->
          <div 
            v-if="isActive(item.path)" 
            class="absolute right-3 w-1.5 h-1.5 rounded-full bg-indigo-600"
          ></div>
        </RouterLink>
      </nav>

      <!-- 底部链接 -->
      <div class="p-4 border-t border-gray-50 space-y-1">
        <div class="px-4 mb-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">
          Actions
        </div>
        <RouterLink
          to="/"
          class="flex items-center gap-3 px-4 py-3 text-gray-500 hover:bg-gray-50 hover:text-gray-900 rounded-xl transition-colors"
        >
          <Home class="w-5 h-5 text-gray-400" />
          <span>返回前台</span>
        </RouterLink>
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-3 px-4 py-3 text-gray-500 hover:bg-red-50 hover:text-red-600 rounded-xl transition-colors group"
        >
          <LogOut class="w-5 h-5 text-gray-400 group-hover:text-red-500" />
          <span>退出登录</span>
        </button>
      </div>
    </aside>

    <!-- 主内容区域 -->
    <div class="flex-1 flex flex-col ml-64 transition-all duration-300">
      <!-- 顶部工具栏 -->
      <header class="h-16 bg-white/80 backdrop-blur-md sticky top-0 z-40 border-b border-gray-100 flex items-center justify-between px-8">
        <!-- 面包屑 -->
        <div class="flex items-center gap-2 text-sm">
          <RouterLink to="/admin" class="text-gray-400 hover:text-indigo-600 transition-colors">后台</RouterLink>
          <ChevronRight class="w-4 h-4 text-gray-300" />
          <span class="font-medium text-gray-900">{{ route.meta.title }}</span>
        </div>

        <!-- 用户信息 -->
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-3 pl-4 border-l border-gray-100">
            <div class="text-right hidden sm:block">
              <div class="text-sm font-medium text-gray-900">{{ userStore.username }}</div>
              <div class="text-xs text-gray-500">{{ userStore.isAdmin ? 'Administrator' : 'User' }}</div>
            </div>
            <div class="w-9 h-9 rounded-full bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center border-2 border-white shadow-sm">
              <span class="text-sm font-bold text-indigo-600">{{ userStore.username.charAt(0).toUpperCase() }}</span>
            </div>
          </div>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="flex-1 p-8">
        <div class="max-w-7xl mx-auto animate-fade-in-up">
          <RouterView />
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
