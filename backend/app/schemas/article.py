"""
文章相关 Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.article import ArticleStatus
from app.schemas.user import UserResponse
from app.schemas.category import CategoryResponse
from app.schemas.tag import TagResponse


class ArticleBase(BaseModel):
    """文章基础 Schema"""
    title: str = Field(..., min_length=1, max_length=200, description="文章标题")
    content: str = Field(..., min_length=1, description="文章内容")
    summary: Optional[str] = Field(None, max_length=500, description="文章摘要")
    cover_image: Optional[str] = Field(None, max_length=255, description="封面图URL")
    status: ArticleStatus = Field(default=ArticleStatus.draft, description="文章状态")
    category_id: Optional[int] = Field(None, description="分类ID")
    tag_ids: Optional[List[int]] = Field(default=[], description="标签ID列表")


class ArticleCreate(ArticleBase):
    """创建文章 Schema"""
    pass


class ArticleUpdate(BaseModel):
    """更新文章 Schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="文章标题")
    content: Optional[str] = Field(None, min_length=1, description="文章内容")
    summary: Optional[str] = Field(None, max_length=500, description="文章摘要")
    cover_image: Optional[str] = Field(None, max_length=255, description="封面图URL")
    status: Optional[ArticleStatus] = Field(None, description="文章状态")
    category_id: Optional[int] = Field(None, description="分类ID")
    tag_ids: Optional[List[int]] = Field(None, description="标签ID列表")


class ArticleResponse(BaseModel):
    """文章响应 Schema"""
    id: int
    title: str
    content: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    status: ArticleStatus
    view_count: int
    user_id: int
    category_id: Optional[int] = None
    author: Optional[UserResponse] = None
    category: Optional[CategoryResponse] = None
    tags: Optional[List[TagResponse]] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    """文章列表响应 Schema"""
    items: List[ArticleResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
