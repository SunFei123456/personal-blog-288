/**
 * 标签相关 API
 * - 标签 CRUD
 */

import { get, post, del } from '@/utils/request'
import type { Tag, TagRequest } from '@/types'

/**
 * 获取标签列表
 * @param userId - 可选，用户ID，筛选指定用户的标签
 * @returns 标签列表
 */
export function getTagsApi(userId?: number): Promise<Tag[]> {
  return get<Tag[]>('/tags', { params: userId ? { user_id: userId } : {} })
}

/**
 * 创建标签
 * @param data - 标签数据
 * @returns 新创建的标签
 */
export function createTagApi(data: TagRequest): Promise<Tag> {
  return post<Tag>('/tags', data)
}

/**
 * 删除标签（管理员）
 * @param id - 标签 ID
 */
export function deleteTagApi(id: number): Promise<void> {
  return del(`/tags/${id}`)
}
