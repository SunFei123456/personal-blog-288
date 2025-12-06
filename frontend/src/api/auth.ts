/**
 * 认证相关 API
 * - 登录
 * - 注册
 * - 获取当前用户信息
 */

import { post, get } from '@/utils/request'
import type { LoginRequest, RegisterRequest, LoginResponse, User } from '@/types'

/**
 * 用户登录
 * @param data - 登录信息（用户名、密码）
 * @returns 登录响应（Token、用户信息）
 */
export function loginApi(data: LoginRequest): Promise<LoginResponse> {
  return post<LoginResponse>('/auth/login', data)
}

/**
 * 用户注册
 * @param data - 注册信息（用户名、邮箱、密码）
 * @returns 新创建的用户信息
 */
export function registerApi(data: RegisterRequest): Promise<User> {
  return post<User>('/auth/register', data)
}

/**
 * 获取当前登录用户信息
 * @returns 当前用户信息
 */
export function getCurrentUserApi(): Promise<User> {
  return get<User>('/auth/me')
}
