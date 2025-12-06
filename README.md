# 个人博客系统

一个基于 Vue3 + FastAPI + MySQL 的前后端分离个人博客系统。

## 技术栈

### 前端
- **框架**: Vue 3.4+ (Composition API)
- **语言**: TypeScript
- **构建工具**: Vite 5.x
- **路由**: Vue Router 4.x
- **状态管理**: Pinia 2.x
- **样式**: TailwindCSS 3.x
- **HTTP客户端**: Axios
- **图标**: Lucide Vue
- **Markdown编辑器**: md-editor-v3

### 后端
- **框架**: FastAPI
- **语言**: Python 3.10+
- **ORM**: SQLAlchemy 2.x
- **数据验证**: Pydantic 2.x
- **认证**: JWT (PyJWT)
- **服务器**: Uvicorn

### 数据库
- **MySQL 8.0**

## 项目结构

```
personal-blog/
├── frontend/          # 前端项目
├── backend/           # 后端项目
├── database/          # 数据库脚本
├── docs/              # 项目文档
└── README.md
```

## 功能模块

### 用户模块
- [x] 用户注册
- [x] 用户登录/登出
- [x] JWT Token 认证
- [x] 角色权限（普通用户/管理员）

### 文章模块
- [x] 文章 CRUD
- [x] 发布/草稿状态
- [x] 分类/标签筛选
- [x] 文章分页
- [x] Markdown 编辑器

### 评论模块
- [x] 评论添加
- [x] 评论删除
- [x] 评论列表

### 后台管理
- [x] 文章管理
- [x] 评论管理
- [x] 分类管理
- [x] 用户管理（管理员）

## 快速开始

### 环境要求
- Node.js 18+
- Python 3.10+
- MySQL 8.0

### 数据库配置

1. 创建数据库：
```sql
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 导入初始化脚本：
```bash
mysql -u root -p blog_db < database/init.sql
```

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（复制 .env.example 为 .env 并修改）
cp .env.example .env

# 启动服务
uvicorn main:app --reload --port 8000
```

后端API文档: http://localhost:8000/docs

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端访问: http://localhost:5173

## API 接口

详见 [API文档](docs/api.md)

## 作者

孙飞

## License

MIT
