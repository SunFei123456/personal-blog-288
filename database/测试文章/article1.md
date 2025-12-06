# Vue3 组合式 API 入门指南

## 前言

Vue3 引入了组合式 API（Composition API），这是一种全新的组织组件逻辑的方式。相比于 Vue2 的选项式 API，组合式 API 提供了更灵活的代码组织能力。

## 什么是组合式 API

组合式 API 是一系列 API 的集合，使我们可以使用函数而不是声明选项的方式书写 Vue 组件。它主要包含以下几个核心概念：

### 1. setup 函数

`setup` 是组合式 API 的入口点，在组件创建之前执行。

```vue
<script setup>
import { ref, onMounted } from 'vue'

const count = ref(0)

onMounted(() => {
  console.log('组件已挂载')
})
</script>
```

### 2. 响应式数据

Vue3 提供了两种创建响应式数据的方式：

- **ref**: 用于基本类型数据
- **reactive**: 用于对象类型数据

```javascript
import { ref, reactive } from 'vue'

// 基本类型使用 ref
const count = ref(0)

// 对象类型使用 reactive
const user = reactive({
  name: '张三',
  age: 25
})
```

### 3. 计算属性

使用 `computed` 函数创建计算属性：

```javascript
import { ref, computed } from 'vue'

const firstName = ref('张')
const lastName = ref('三')

const fullName = computed(() => {
  return firstName.value + lastName.value
})
```

## 为什么使用组合式 API

1. **更好的代码组织**: 相关逻辑可以放在一起
2. **更好的类型推断**: 对 TypeScript 更友好
3. **更小的打包体积**: 更好的 Tree-shaking
4. **逻辑复用**: 通过组合函数轻松复用逻辑

## 总结

组合式 API 是 Vue3 的重要特性，它让我们能够更灵活地组织代码，提高代码的可维护性和复用性。如果你正在开始一个新的 Vue 项目，强烈建议使用组合式 API。

---

*本文是 Vue3 系列教程的第一篇，后续将继续介绍更多 Vue3 的高级特性。*
