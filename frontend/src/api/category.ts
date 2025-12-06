/**
 * 分类相关 API
 * - 分类 CRUD
 */

import { get, post, put, del } from '@/utils/request'
import type { Category, CategoryRequest } from '@/types'

/**
 * 获取分类列表
 * @param userId - 可选，用户ID，筛选指定用户的分类
 * @returns 分类列表
 */
export function getCategoriesApi(userId?: number): Promise<Category[]> {
  return get<Category[]>('/categories', { params: userId ? { user_id: userId } : {} })
}

/**
 * 获取分类详情
 * @param id - 分类 ID
 * @returns 分类详情
 */
export function getCategoryApi(id: number): Promise<Category> {
  return get<Category>(`/categories/${id}`)
}

/**
 * 创建分类（管理员）
 * @param data - 分类数据
 * @returns 新创建的分类
 */
export function createCategoryApi(data: CategoryRequest): Promise<Category> {
  return post<Category>('/categories', data)
}

/**
 * 更新分类（管理员）
 * @param id - 分类 ID
 * @param data - 更新的分类数据
 * @returns 更新后的分类
 */
export function updateCategoryApi(id: number, data: CategoryRequest): Promise<Category> {
  return put<Category>(`/categories/${id}`, data)
}

/**
 * 删除分类（管理员）
 * @param id - 分类 ID
 */
export function deleteCategoryApi(id: number): Promise<void> {
  return del(`/categories/${id}`)
}
