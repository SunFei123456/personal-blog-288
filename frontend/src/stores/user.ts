/**
 * 用户状态管理
 * - 管理用户登录状态
 * - 管理 Token
 * - 提供登录/登出方法
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginRequest, RegisterRequest, LoginResponse } from '@/types'
import { post, get } from '@/utils/request'

/**
 * 用户状态 Store
 */
export const useUserStore = defineStore('user', () => {
  // ==================== 状态 ====================
  
  /** 当前用户信息 */
  const user = ref<User | null>(null)
  
  /** 访问令牌 */
  const token = ref<string>(localStorage.getItem('token') || '')

  // ==================== 计算属性 ====================
  
  /** 是否已登录 */
  const isLoggedIn = computed(() => !!token.value)
  
  /** 是否是管理员 */
  const isAdmin = computed(() => user.value?.role === 'admin')
  
  /** 用户名 */
  const username = computed(() => user.value?.username || '')

  // ==================== 方法 ====================
  
  /**
   * 设置 Token
   * @param newToken - 新的访问令牌
   */
  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  /**
   * 清除 Token
   */
  function clearToken() {
    token.value = ''
    localStorage.removeItem('token')
  }

  /**
   * 用户登录
   * @param loginData - 登录信息
   */
  async function login(loginData: LoginRequest): Promise<LoginResponse> {
    const response = await post<LoginResponse>('/auth/login', loginData)
    setToken(response.access_token)
    user.value = response.user
    return response
  }

  /**
   * 用户注册
   * @param registerData - 注册信息
   */
  async function register(registerData: RegisterRequest): Promise<User> {
    const response = await post<User>('/auth/register', registerData)
    return response
  }

  /**
   * 获取当前用户信息
   */
  async function fetchUserInfo(): Promise<User> {
    const response = await get<User>('/auth/me')
    user.value = response
    return response
  }

  /**
   * 用户登出
   */
  function logout() {
    user.value = null
    clearToken()
  }

  /**
   * 初始化用户状态
   * - 如果有 Token，尝试获取用户信息
   */
  async function initUser() {
    if (token.value) {
      try {
        await fetchUserInfo()
      } catch (error) {
        // Token 无效，清除登录状态
        logout()
      }
    }
  }

  return {
    // 状态
    user,
    token,
    // 计算属性
    isLoggedIn,
    isAdmin,
    username,
    // 方法
    setToken,
    clearToken,
    login,
    register,
    fetchUserInfo,
    logout,
    initUser,
  }
})
