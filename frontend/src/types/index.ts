/**
 * 类型定义文件
 * 定义项目中使用的所有 TypeScript 类型
 */

// ==================== 用户相关类型 ====================

/**
 * 用户角色枚举
 */
export type UserRole = 'user' | 'admin'

/**
 * 用户信息接口
 */
export interface User {
  id: number
  username: string
  email: string
  avatar?: string
  role: UserRole
  created_at: string
  updated_at: string
}

/**
 * 登录请求参数
 */
export interface LoginRequest {
  username: string
  password: string
}

/**
 * 注册请求参数
 */
export interface RegisterRequest {
  username: string
  email: string
  password: string
}

/**
 * 登录响应
 */
export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

// ==================== 文章相关类型 ====================

/**
 * 文章状态枚举
 */
export type ArticleStatus = 'draft' | 'published'

/**
 * 文章信息接口
 */
export interface Article {
  id: number
  title: string
  content: string
  summary: string
  cover_image?: string
  status: ArticleStatus
  view_count: number
  user_id: number
  category_id?: number
  author?: User
  category?: Category
  tags?: Tag[]
  created_at: string
  updated_at: string
}

/**
 * 创建/更新文章请求参数
 */
export interface ArticleRequest {
  title: string
  content: string
  summary?: string
  cover_image?: string
  status: ArticleStatus
  category_id?: number
  tag_ids?: number[]
}

/**
 * 文章查询参数
 */
export interface ArticleQuery {
  page?: number
  page_size?: number
  status?: ArticleStatus
  category_id?: number
  tag_id?: number
  keyword?: string
  user_id?: number
}

// ==================== 分类相关类型 ====================

/**
 * 分类信息接口
 */
export interface Category {
  id: number
  name: string
  description?: string
  article_count?: number
  created_at: string
}

/**
 * 创建/更新分类请求参数
 */
export interface CategoryRequest {
  name: string
  description?: string
}

// ==================== 标签相关类型 ====================

/**
 * 标签信息接口
 */
export interface Tag {
  id: number
  name: string
  article_count?: number
}

/**
 * 创建标签请求参数
 */
export interface TagRequest {
  name: string
}

// ==================== 评论相关类型 ====================

/**
 * 评论信息接口
 */
export interface Comment {
  id: number
  content: string
  article_id: number
  user_id: number
  user?: User
  created_at: string
}

/**
 * 创建评论请求参数
 */
export interface CommentRequest {
  content: string
}

// ==================== 通用类型 ====================

/**
 * 分页响应接口
 */
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

/**
 * API 响应接口
 */
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

/**
 * 统计数据接口（后台首页）
 */
export interface Statistics {
  user_count: number
  article_count: number
  comment_count: number
  view_count: number
}
