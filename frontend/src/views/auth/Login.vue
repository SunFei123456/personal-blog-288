<script setup lang="ts">
/**
 * 登录页面
 * - 用户名/密码登录
 * - 表单验证
 * - 登录成功跳转
 */

import { ref, reactive } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { LogIn, User, Lock, Loader2 } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

/** 表单数据 */
const form = reactive({
  username: '',
  password: '',
})

/** 加载状态 */
const loading = ref(false)

/** 错误信息 */
const errorMsg = ref('')

/**
 * 处理登录提交
 */
async function handleSubmit() {
  // 表单验证
  if (!form.username.trim()) {
    errorMsg.value = '请输入用户名'
    return
  }
  if (!form.password) {
    errorMsg.value = '请输入密码'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    await userStore.login({
      username: form.username,
      password: form.password,
    })

    // 登录成功，跳转到之前的页面或首页
    const redirect = route.query.redirect as string || '/'
    router.push(redirect)
  } catch (error: any) {
    errorMsg.value = error.response?.data?.detail || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
    <div class="max-w-md w-full">
      <!-- 标题 -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">欢迎回来</h1>
        <p class="mt-2 text-gray-600">登录您的账户继续</p>
      </div>

      <!-- 登录表单 -->
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- 错误提示 -->
          <div
            v-if="errorMsg"
            class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm"
          >
            {{ errorMsg }}
          </div>

          <!-- 用户名输入 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
            <div class="relative">
              <User class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.username"
                type="text"
                placeholder="请输入用户名"
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
              />
            </div>
          </div>

          <!-- 密码输入 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">密码</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.password"
                type="password"
                placeholder="请输入密码"
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
              />
            </div>
          </div>

          <!-- 登录按钮 -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex items-center justify-center gap-2 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
            <LogIn v-else class="w-5 h-5" />
            <span>{{ loading ? '登录中...' : '登录' }}</span>
          </button>
        </form>

        <!-- 注册链接 -->
        <div class="mt-6 text-center text-gray-600">
          还没有账户？
          <RouterLink to="/register" class="text-blue-600 hover:text-blue-800 font-medium">
            立即注册
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>
