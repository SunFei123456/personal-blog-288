/**
 * Vue Router 路由配置
 * - 前台页面路由
 * - 后台管理路由
 * - 路由守卫
 */

import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

/**
 * 路由配置
 */
const routes: RouteRecordRaw[] = [
  // ==================== 前台页面 ====================
  {
    path: '/',
    component: () => import('@/layouts/FrontLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/blog/Home.vue'),
        meta: { title: '首页' },
      },
      {
        path: 'article/:id',
        name: 'ArticleDetail',
        component: () => import('@/views/blog/ArticleDetail.vue'),
        meta: { title: '文章详情' },
      },
      {
        path: 'category/:id',
        name: 'CategoryArticles',
        component: () => import('@/views/blog/CategoryArticles.vue'),
        meta: { title: '分类文章' },
      },
      {
        path: 'tag/:id',
        name: 'TagArticles',
        component: () => import('@/views/blog/TagArticles.vue'),
        meta: { title: '标签文章' },
      },
    ],
  },

  // ==================== 认证页面 ====================
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { title: '登录', guest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { title: '注册', guest: true },
  },

  // ==================== 后台管理 ====================
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '控制台' },
      },
      {
        path: 'articles',
        name: 'AdminArticles',
        component: () => import('@/views/admin/Articles.vue'),
        meta: { title: '文章管理' },
      },
      {
        path: 'articles/edit/:id?',
        name: 'AdminArticleEdit',
        component: () => import('@/views/admin/ArticleEdit.vue'),
        meta: { title: '编辑文章' },
      },
      {
        path: 'categories',
        name: 'AdminCategories',
        component: () => import('@/views/admin/Categories.vue'),
        meta: { title: '分类管理' },
      },
      {
        path: 'tags',
        name: 'AdminTags',
        component: () => import('@/views/admin/Tags.vue'),
        meta: { title: '标签管理' },
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/Users.vue'),
        meta: { title: '用户管理', requiresAdmin: true },
      },
    ],
  },

  // ==================== 404 页面 ====================
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面不存在' },
  },
]

/**
 * 创建路由实例
 */
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

/**
 * 路由守卫
 * - 检查登录状态
 * - 检查管理员权限
 * - 设置页面标题
 */
router.beforeEach(async (to, _from, next) => {
  const userStore = useUserStore()

  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 个人博客` : '个人博客'

  // 如果有 Token 但没有用户信息，尝试获取
  if (userStore.token && !userStore.user) {
    try {
      await userStore.fetchUserInfo()
    } catch {
      userStore.logout()
    }
  }

  // 已登录用户访问登录/注册页，重定向到首页
  if (to.meta.guest && userStore.isLoggedIn) {
    return next('/')
  }

  // 需要登录的页面
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  // 需要管理员权限的页面
  if (to.meta.requiresAdmin && !userStore.isAdmin) {
    return next('/admin')
  }

  next()
})

export default router

/**
 * 路由 meta 类型扩展
 */
declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    requiresAuth?: boolean
    requiresAdmin?: boolean
    guest?: boolean
  }
}
