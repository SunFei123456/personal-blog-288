/**
 * Axios 请求封装
 * - 统一请求/响应拦截
 * - Token 自动携带
 * - 错误统一处理
 */

import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'
import router from '@/router'

/**
 * 创建 Axios 实例
 */
const request: AxiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * 请求拦截器
 * - 自动携带 Token
 * - 直接从 localStorage 读取，避免 Pinia 初始化问题
 */
request.interceptors.request.use(
  (config) => {
    // 直接从 localStorage 读取 token，避免循环依赖和初始化问题
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 * - 统一处理响应数据
 * - 处理认证失败
 */
request.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data
  },
  (error) => {
    const { response } = error
    
    if (response) {
      switch (response.status) {
        case 401:
          // Token 过期或无效
          // 注意：不在这里清除 token 和跳转，让路由守卫统一处理
          // 避免在 fetchUserInfo 时误清除刚保存的 token
          console.error('认证失败，请重新登录')
          break
        case 403:
          console.error('没有权限访问该资源')
          break
        case 404:
          console.error('请求的资源不存在')
          break
        case 500:
          console.error('服务器内部错误')
          break
        default:
          console.error('请求失败:', response.data?.detail || '未知错误')
      }
    } else {
      console.error('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

export default request

/**
 * GET 请求封装
 */
export function get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
  return request.get(url, config)
}

/**
 * POST 请求封装
 */
export function post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
  return request.post(url, data, config)
}

/**
 * PUT 请求封装
 */
export function put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
  return request.put(url, data, config)
}

/**
 * DELETE 请求封装
 */
export function del<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
  return request.delete(url, config)
}
