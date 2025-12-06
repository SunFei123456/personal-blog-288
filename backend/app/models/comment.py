"""
评论模型
"""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Comment(Base):
    """
    评论表模型
    
    Attributes:
        id: 主键
        content: 评论内容
        article_id: 文章 ID
        user_id: 用户 ID
        created_at: 创建时间
    """
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(Text, nullable=False, comment="评论内容")
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, comment="文章ID")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    # 关联关系
    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")
