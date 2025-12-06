"""
标签相关 Schema
"""

from pydantic import BaseModel, Field
from typing import Optional


class TagBase(BaseModel):
    """标签基础 Schema"""
    name: str = Field(..., min_length=1, max_length=50, description="标签名称")


class TagCreate(TagBase):
    """创建标签 Schema"""
    pass


class TagResponse(TagBase):
    """标签响应 Schema"""
    id: int
    article_count: Optional[int] = 0
    
    class Config:
        from_attributes = True
