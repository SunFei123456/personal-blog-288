<script setup lang="ts">
/**
 * 根组件
 * - 初始化用户状态
 * - 渲染路由视图
 */

import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 应用启动时初始化用户状态
onMounted(() => {
  userStore.initUser()
})
</script>

<template>
  <RouterView />
</template>
