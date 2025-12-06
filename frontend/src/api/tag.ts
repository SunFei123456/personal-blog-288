/**
 * 标签相关 API
 * - 标签 CRUD
 */

import { get, post, del } from '@/utils/request'
import type { Tag, TagRequest } from '@/types'

/**
 * 获取标签列表
 * @returns 标签列表
 */
export function getTagsApi(): Promise<Tag[]> {
  return get<Tag[]>('/tags')
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
