<script setup lang="ts">
/**
 * 注册页面
 * - 用户注册表单
 * - 表单验证
 * - 注册成功跳转登录
 */

import { ref, reactive } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { UserPlus, User, Mail, Lock, Loader2 } from 'lucide-vue-next'

const router = useRouter()
const userStore = useUserStore()

/** 表单数据 */
const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
})

/** 加载状态 */
const loading = ref(false)

/** 错误信息 */
const errorMsg = ref('')

/** 成功信息 */
const successMsg = ref('')

/**
 * 验证邮箱格式
 */
function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * 处理注册提交
 */
async function handleSubmit() {
  // 表单验证
  if (!form.username.trim()) {
    errorMsg.value = '请输入用户名'
    return
  }
  if (form.username.length < 3 || form.username.length > 20) {
    errorMsg.value = '用户名长度应在 3-20 个字符之间'
    return
  }
  if (!form.email.trim()) {
    errorMsg.value = '请输入邮箱'
    return
  }
  if (!isValidEmail(form.email)) {
    errorMsg.value = '请输入有效的邮箱地址'
    return
  }
  if (!form.password) {
    errorMsg.value = '请输入密码'
    return
  }
  if (form.password.length < 6) {
    errorMsg.value = '密码长度至少 6 个字符'
    return
  }
  if (form.password !== form.confirmPassword) {
    errorMsg.value = '两次输入的密码不一致'
    return
  }

  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''

  try {
    await userStore.register({
      username: form.username,
      email: form.email,
      password: form.password,
    })

    successMsg.value = '注册成功！即将跳转到登录页面...'
    
    // 延迟跳转到登录页
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (error: any) {
    errorMsg.value = error.response?.data?.detail || '注册失败，请稍后重试'
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
        <h1 class="text-3xl font-bold text-gray-900">创建账户</h1>
        <p class="mt-2 text-gray-600">注册一个新账户开始使用</p>
      </div>

      <!-- 注册表单 -->
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <!-- 错误提示 -->
          <div
            v-if="errorMsg"
            class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm"
          >
            {{ errorMsg }}
          </div>

          <!-- 成功提示 -->
          <div
            v-if="successMsg"
            class="p-4 bg-green-50 border border-green-200 rounded-lg text-green-600 text-sm"
          >
            {{ successMsg }}
          </div>

          <!-- 用户名输入 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
            <div class="relative">
              <User class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.username"
                type="text"
                placeholder="请输入用户名（3-20个字符）"
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
              />
            </div>
          </div>

          <!-- 邮箱输入 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.email"
                type="email"
                placeholder="请输入邮箱地址"
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
                placeholder="请输入密码（至少6个字符）"
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
              />
            </div>
          </div>

          <!-- 确认密码输入 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">确认密码</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.confirmPassword"
                type="password"
                placeholder="请再次输入密码"
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
              />
            </div>
          </div>

          <!-- 注册按钮 -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex items-center justify-center gap-2 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
            <UserPlus v-else class="w-5 h-5" />
            <span>{{ loading ? '注册中...' : '注册' }}</span>
          </button>
        </form>

        <!-- 登录链接 -->
        <div class="mt-6 text-center text-gray-600">
          已有账户？
          <RouterLink to="/login" class="text-blue-600 hover:text-blue-800 font-medium">
            立即登录
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>
