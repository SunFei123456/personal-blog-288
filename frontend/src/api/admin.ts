/**
 * 管理员相关 API
 * - 用户管理
 * - 统计数据
 */

import { get, put, del } from '@/utils/request'
import type { User, PaginatedResponse, Statistics } from '@/types'

/**
 * 获取统计数据
 * @returns 统计数据
 */
export function getStatisticsApi(): Promise<Statistics> {
  return get<Statistics>('/admin/statistics')
}

/**
 * 获取用户列表
 * @param page - 页码
 * @param pageSize - 每页数量
 * @returns 分页用户列表
 */
export function getUsersApi(
  page: number = 1,
  pageSize: number = 20
): Promise<PaginatedResponse<User>> {
  return get<PaginatedResponse<User>>('/admin/users', {
    params: { page, page_size: pageSize },
  })
}

/**
 * 更新用户信息
 * @param id - 用户 ID
 * @param data - 更新的用户数据
 * @returns 更新后的用户
 */
export function updateUserApi(id: number, data: Partial<User>): Promise<User> {
  return put<User>(`/admin/users/${id}`, data)
}

/**
 * 删除用户
 * @param id - 用户 ID
 */
export function deleteUserApi(id: number): Promise<void> {
  return del(`/admin/users/${id}`)
}
