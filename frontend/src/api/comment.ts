/**
 * 评论相关 API
 * - 评论 CRUD
 */

import { get, post, del } from '@/utils/request'
import type { Comment, CommentRequest, PaginatedResponse } from '@/types'

/**
 * 获取文章的评论列表
 * @param articleId - 文章 ID
 * @param page - 页码
 * @param pageSize - 每页数量
 * @returns 分页评论列表
 */
export function getCommentsApi(
  articleId: number,
  page: number = 1,
  pageSize: number = 20
): Promise<PaginatedResponse<Comment>> {
  return get<PaginatedResponse<Comment>>(`/articles/${articleId}/comments`, {
    params: { page, page_size: pageSize },
  })
}

/**
 * 创建评论
 * @param articleId - 文章 ID
 * @param data - 评论数据
 * @returns 新创建的评论
 */
export function createCommentApi(articleId: number, data: CommentRequest): Promise<Comment> {
  return post<Comment>(`/articles/${articleId}/comments`, data)
}

/**
 * 删除评论
 * @param id - 评论 ID
 */
export function deleteCommentApi(id: number): Promise<void> {
  return del(`/comments/${id}`)
}

/**
 * 获取所有评论列表（管理员）
 * @param page - 页码
 * @param pageSize - 每页数量
 * @returns 分页评论列表
 */
export function getAllCommentsApi(
  page: number = 1,
  pageSize: number = 20
): Promise<PaginatedResponse<Comment>> {
  return get<PaginatedResponse<Comment>>('/admin/comments', {
    params: { page, page_size: pageSize },
  })
}
