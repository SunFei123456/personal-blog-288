/**
 * 应用入口文件
 * - 初始化 Vue 应用
 * - 注册 Pinia 状态管理
 * - 注册 Vue Router 路由
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

// 创建 Vue 应用实例
const app = createApp(App)

// 注册 Pinia 状态管理
const pinia = createPinia()
app.use(pinia)

// 注册 Vue Router
app.use(router)

// 挂载应用
app.mount('#app')
