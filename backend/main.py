"""
FastAPI 应用入口
- 创建应用实例
- 注册路由
- 配置中间件
- 创建数据库表
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.db.database import engine, Base
from app.models import User, Category, Tag, Article, Comment  # 导入所有模型以创建表


# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title="个人博客系统 API",
    description="基于 FastAPI 的个人博客系统后端 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["根路径"])
def root():
    """
    根路径
    返回 API 基本信息
    """
    return {
        "message": "欢迎使用个人博客系统 API",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health", tags=["健康检查"])
def health_check():
    """
    健康检查接口
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
