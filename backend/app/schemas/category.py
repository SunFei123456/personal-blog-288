"""
分类相关 Schema
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    """分类基础 Schema"""
    name: str = Field(..., min_length=1, max_length=50, description="分类名称")
    description: Optional[str] = Field(None, max_length=255, description="分类描述")


class CategoryCreate(CategoryBase):
    """创建分类 Schema"""
    pass


class CategoryUpdate(BaseModel):
    """更新分类 Schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="分类名称")
    description: Optional[str] = Field(None, max_length=255, description="分类描述")


class CategoryResponse(CategoryBase):
    """分类响应 Schema"""
    id: int
    article_count: Optional[int] = 0
    created_at: datetime
    
    class Config:
        from_attributes = True
