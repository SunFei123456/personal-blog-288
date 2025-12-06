"""
评论相关 Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.user import UserResponse


class CommentBase(BaseModel):
    """评论基础 Schema"""
    content: str = Field(..., min_length=1, max_length=1000, description="评论内容")


class CommentCreate(CommentBase):
    """创建评论 Schema"""
    pass


class CommentResponse(CommentBase):
    """评论响应 Schema"""
    id: int
    article_id: int
    user_id: int
    user: Optional[UserResponse] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    """评论列表响应 Schema"""
    items: List[CommentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
