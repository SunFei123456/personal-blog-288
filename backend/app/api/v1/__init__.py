"""
API v1 路由模块
"""

from fastapi import APIRouter
from app.api.v1 import auth, articles, categories, tags, admin


# 创建 API v1 路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(auth.router)
api_router.include_router(articles.router)
api_router.include_router(categories.router)
api_router.include_router(tags.router)
api_router.include_router(admin.router)
