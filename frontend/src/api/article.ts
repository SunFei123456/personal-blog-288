/**
 * 文章相关 API
 * - 文章 CRUD
 * - 文章列表查询
 */

import { get, post, put, del } from '@/utils/request'
import type { Article, ArticleRequest, ArticleQuery, PaginatedResponse } from '@/types'

/**
 * 获取文章列表
 * @param params - 查询参数（分页、筛选条件）
 * @returns 分页文章列表
 */
export function getArticlesApi(params?: ArticleQuery): Promise<PaginatedResponse<Article>> {
  return get<PaginatedResponse<Article>>('/articles', { params })
}

/**
 * 获取文章详情
 * @param id - 文章 ID
 * @returns 文章详情
 */
export function getArticleApi(id: number): Promise<Article> {
  return get<Article>(`/articles/${id}`)
}

/**
 * 创建文章
 * @param data - 文章数据
 * @returns 新创建的文章
 */
export function createArticleApi(data: ArticleRequest): Promise<Article> {
  return post<Article>('/articles', data)
}

/**
 * 更新文章
 * @param id - 文章 ID
 * @param data - 更新的文章数据
 * @returns 更新后的文章
 */
export function updateArticleApi(id: number, data: ArticleRequest): Promise<Article> {
  return put<Article>(`/articles/${id}`, data)
}

/**
 * 删除文章
 * @param id - 文章 ID
 */
export function deleteArticleApi(id: number): Promise<void> {
  return del(`/articles/${id}`)
}

/**
 * 获取用户的文章列表
 * @param params - 查询参数
 * @returns 分页文章列表
 */
export function getMyArticlesApi(params?: ArticleQuery): Promise<PaginatedResponse<Article>> {
  return get<PaginatedResponse<Article>>('/articles/my', { params })
}
