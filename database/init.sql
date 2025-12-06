-- =====================================================
-- 个人博客系统数据库初始化脚本
-- 数据库: MySQL 8.0
-- 字符集: utf8mb4
-- =====================================================

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS blog_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE blog_db;

-- =====================================================
-- 用户表
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    avatar VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
    role ENUM('user', 'admin') DEFAULT 'user' NOT NULL COMMENT '用户角色',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- =====================================================
-- 分类表
-- =====================================================
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '分类ID',
    name VARCHAR(50) NOT NULL COMMENT '分类名称',
    description VARCHAR(255) DEFAULT NULL COMMENT '分类描述',
    user_id INT NOT NULL COMMENT '所属用户ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    UNIQUE KEY uq_category_user_name (user_id, name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='分类表';

-- =====================================================
-- 标签表
-- =====================================================
CREATE TABLE IF NOT EXISTS tags (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '标签ID',
    name VARCHAR(50) NOT NULL COMMENT '标签名称',
    user_id INT NOT NULL COMMENT '所属用户ID',
    INDEX idx_user_id (user_id),
    UNIQUE KEY uq_tag_user_name (user_id, name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='标签表';

-- =====================================================
-- 文章表
-- =====================================================
CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '文章ID',
    title VARCHAR(200) NOT NULL COMMENT '文章标题',
    content TEXT NOT NULL COMMENT '文章内容',
    summary VARCHAR(500) DEFAULT NULL COMMENT '文章摘要',
    cover_image VARCHAR(255) DEFAULT NULL COMMENT '封面图URL',
    status ENUM('draft', 'published') DEFAULT 'draft' NOT NULL COMMENT '文章状态',
    view_count INT DEFAULT 0 NOT NULL COMMENT '浏览量',
    user_id INT NOT NULL COMMENT '作者ID',
    category_id INT DEFAULT NULL COMMENT '分类ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_id (user_id),
    INDEX idx_category_id (category_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文章表';

-- =====================================================
-- 文章标签关联表
-- =====================================================
CREATE TABLE IF NOT EXISTS article_tags (
    article_id INT NOT NULL COMMENT '文章ID',
    tag_id INT NOT NULL COMMENT '标签ID',
    PRIMARY KEY (article_id, tag_id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文章标签关联表';


-- =====================================================
-- 初始数据
-- =====================================================

-- 插入管理员用户（密码: admin123）
-- 密码哈希使用 bcrypt 生成
INSERT INTO users (username, email, password_hash, role) VALUES 
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYWWQXQK.Qm2', 'admin')
ON DUPLICATE KEY UPDATE username = username;

-- 插入普通用户（密码: user123）
INSERT INTO users (username, email, password_hash, role) VALUES 
('user', 'user@example.com', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'user')
ON DUPLICATE KEY UPDATE username = username;

-- 插入示例分类（绑定到管理员用户）
INSERT INTO categories (name, description, user_id) VALUES 
('技术', '技术相关文章', 1),
('生活', '生活随笔', 1),
('学习', '学习笔记', 1)
ON DUPLICATE KEY UPDATE name = name;

-- 插入示例标签（绑定到管理员用户）
INSERT INTO tags (name, user_id) VALUES 
('Vue', 1),
('Python', 1),
('FastAPI', 1),
('MySQL', 1),
('前端', 1),
('后端', 1)
ON DUPLICATE KEY UPDATE name = name;

-- 插入示例文章
INSERT INTO articles (title, content, summary, status, user_id, category_id) VALUES 
('欢迎使用个人博客系统', 
'# 欢迎使用个人博客系统

这是一个基于 **Vue3 + FastAPI + MySQL** 构建的个人博客系统。

## 功能特点

- 用户注册、登录
- 文章发布、编辑、删除
- 评论功能
- 分类和标签管理
- 后台管理系统

## 技术栈

### 前端
- Vue 3
- TypeScript
- TailwindCSS
- Pinia
- Vue Router

### 后端
- FastAPI
- SQLAlchemy
- JWT 认证

### 数据库
- MySQL 8.0

欢迎使用！', 
'这是一个基于 Vue3 + FastAPI + MySQL 构建的个人博客系统。',
'published', 1, 1)
ON DUPLICATE KEY UPDATE title = title;

-- 为示例文章添加标签
INSERT INTO article_tags (article_id, tag_id) VALUES 
(1, 1), (1, 2), (1, 3)
ON DUPLICATE KEY UPDATE article_id = article_id;


-- =====================================================
-- 完成
-- =====================================================
SELECT '数据库初始化完成！' AS message;
