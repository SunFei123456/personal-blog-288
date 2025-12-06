<script setup lang="ts">
/**
 * 前台布局组件
 * - 顶部导航栏
 * - 主内容区域
 * - 底部版权信息
 */

import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { BookOpen, Home, LogIn, LogOut, Settings, User } from 'lucide-vue-next'

const userStore = useUserStore()

/**
 * 处理登出
 */
function handleLogout() {
  userStore.logout()
}
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <nav class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2 text-xl font-bold text-gray-900 hover:text-blue-600">
          <BookOpen class="w-6 h-6" />
          <span>个人博客</span>
        </RouterLink>

        <!-- 导航链接 -->
        <div class="flex items-center gap-6">
          <RouterLink to="/" class="flex items-center gap-1 text-gray-600 hover:text-blue-600">
            <Home class="w-4 h-4" />
            <span>首页</span>
          </RouterLink>

          <!-- 已登录状态 -->
          <template v-if="userStore.isLoggedIn">
            <RouterLink to="/admin" class="flex items-center gap-1 text-gray-600 hover:text-blue-600">
              <Settings class="w-4 h-4" />
              <span>管理后台</span>
            </RouterLink>
            
            <div class="flex items-center gap-3">
              <span class="text-gray-600 flex items-center gap-1">
                <User class="w-4 h-4" />
                {{ userStore.username }}
              </span>
              <button
                @click="handleLogout"
                class="flex items-center gap-1 text-gray-600 hover:text-red-600"
              >
                <LogOut class="w-4 h-4" />
                <span>登出</span>
              </button>
            </div>
          </template>

          <!-- 未登录状态 -->
          <template v-else>
            <RouterLink to="/login" class="flex items-center gap-1 text-gray-600 hover:text-blue-600">
              <LogIn class="w-4 h-4" />
              <span>登录</span>
            </RouterLink>
            <RouterLink
              to="/register"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              注册
            </RouterLink>
          </template>
        </div>
      </nav>
    </header>

    <!-- 主内容区域 -->
    <main class="flex-1">
      <RouterView />
    </main>

    <!-- 底部版权信息 -->
    <footer class="bg-gray-100 border-t border-gray-200 py-6">
      <div class="max-w-6xl mx-auto px-4 text-center text-gray-500 text-sm">
        <p>© 2024 个人博客系统. All rights reserved.</p>
        <p class="mt-1">基于 Vue3 + FastAPI + MySQL 构建</p>
      </div>
    </footer>
  </div>
</template>
