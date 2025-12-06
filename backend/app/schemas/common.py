"""
通用 Schema
"""

from pydantic import BaseModel
from typing import Optional


class Statistics(BaseModel):
    """统计数据 Schema"""
    user_count: int = 0
    article_count: int = 0
    comment_count: int = 0
    view_count: int = 0


class MessageResponse(BaseModel):
    """消息响应 Schema"""
    message: str
    detail: Optional[str] = None
