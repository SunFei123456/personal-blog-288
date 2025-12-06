# API 接口文档

## 基础信息

- **基础路径**: `/api/v1`
- **认证方式**: JWT Bearer Token
- **响应格式**: JSON

---

## 认证模块

### 用户注册

**POST** `/api/v1/auth/register`

**请求参数**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

**成功响应** (200):
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "avatar": null,
  "role": "user",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

### 用户登录

**POST** `/api/v1/auth/login`

**请求参数**:
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**成功响应** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "avatar": null,
    "role": "user",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

---

### 获取当前用户信息

**GET** `/api/v1/auth/me`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "avatar": null,
  "role": "user",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

## 文章模块

### 获取文章列表

**GET** `/api/v1/articles`

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认 1 |
| page_size | int | 否 | 每页数量，默认 10 |
| status | string | 否 | 文章状态 (draft/published) |
| category_id | int | 否 | 分类 ID |
| tag_id | int | 否 | 标签 ID |
| keyword | string | 否 | 搜索关键词 |

**成功响应** (200):
```json
{
  "items": [
    {
      "id": 1,
      "title": "文章标题",
      "content": "文章内容...",
      "summary": "文章摘要",
      "cover_image": null,
      "status": "published",
      "view_count": 100,
      "user_id": 1,
      "category_id": 1,
      "author": { "id": 1, "username": "admin", ... },
      "category": { "id": 1, "name": "技术", ... },
      "tags": [{ "id": 1, "name": "Vue" }],
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

---

### 获取文章详情

**GET** `/api/v1/articles/{article_id}`

**成功响应** (200):
```json
{
  "id": 1,
  "title": "文章标题",
  "content": "文章内容...",
  "summary": "文章摘要",
  "cover_image": null,
  "status": "published",
  "view_count": 101,
  "user_id": 1,
  "category_id": 1,
  "author": { "id": 1, "username": "admin", ... },
  "category": { "id": 1, "name": "技术", ... },
  "tags": [{ "id": 1, "name": "Vue" }],
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

### 创建文章

**POST** `/api/v1/articles`

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "title": "文章标题",
  "content": "文章内容（支持 Markdown）",
  "summary": "文章摘要（可选）",
  "cover_image": "封面图 URL（可选）",
  "status": "draft",
  "category_id": 1,
  "tag_ids": [1, 2]
}
```

**成功响应** (200): 返回创建的文章对象

---

### 更新文章

**PUT** `/api/v1/articles/{article_id}`

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**: 同创建文章，所有字段可选

**成功响应** (200): 返回更新后的文章对象

---

### 删除文章

**DELETE** `/api/v1/articles/{article_id}`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "message": "文章已删除"
}
```

---

## 分类模块

### 获取分类列表

**GET** `/api/v1/categories`

**成功响应** (200):
```json
[
  {
    "id": 1,
    "name": "技术",
    "description": "技术相关文章",
    "article_count": 10,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### 创建分类（管理员）

**POST** `/api/v1/categories`

**请求头**:
```
Authorization: Bearer <admin_token>
```

**请求参数**:
```json
{
  "name": "分类名称",
  "description": "分类描述（可选）"
}
```

---

## 标签模块

### 获取标签列表

**GET** `/api/v1/tags`

**成功响应** (200):
```json
[
  {
    "id": 1,
    "name": "Vue",
    "article_count": 5
  }
]
```

---

### 创建标签

**POST** `/api/v1/tags`

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "name": "标签名称"
}
```

---

## 评论模块

### 获取文章评论

**GET** `/api/v1/articles/{article_id}/comments`

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认 1 |
| page_size | int | 否 | 每页数量，默认 20 |

**成功响应** (200):
```json
{
  "items": [
    {
      "id": 1,
      "content": "评论内容",
      "article_id": 1,
      "user_id": 1,
      "user": { "id": 1, "username": "user", ... },
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "total_pages": 1
}
```

---

### 添加评论

**POST** `/api/v1/articles/{article_id}/comments`

**请求头**:
```
Authorization: Bearer <token>
```

**请求参数**:
```json
{
  "content": "评论内容"
}
```

---

### 删除评论

**DELETE** `/api/v1/comments/{comment_id}`

**请求头**:
```
Authorization: Bearer <token>
```

**成功响应** (200):
```json
{
  "message": "评论已删除"
}
```

---

## 管理员模块

### 获取统计数据

**GET** `/api/v1/admin/statistics`

**请求头**:
```
Authorization: Bearer <admin_token>
```

**成功响应** (200):
```json
{
  "user_count": 10,
  "article_count": 50,
  "comment_count": 100,
  "view_count": 5000
}
```

---

### 获取用户列表

**GET** `/api/v1/admin/users`

**请求头**:
```
Authorization: Bearer <admin_token>
```

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认 1 |
| page_size | int | 否 | 每页数量，默认 20 |

---

## 错误响应

所有接口在发生错误时返回统一格式：

```json
{
  "detail": "错误信息描述"
}
```

**常见状态码**:
- `400` - 请求参数错误
- `401` - 未认证或认证失败
- `403` - 权限不足
- `404` - 资源不存在
- `500` - 服务器内部错误
