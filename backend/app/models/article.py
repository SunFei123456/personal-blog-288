"""
文章模型
"""

from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
from app.models.tag import article_tags
import enum


class ArticleStatus(str, enum.Enum):
    """文章状态枚举"""
    draft = "draft"
    published = "published"


class Article(Base):
    """
    文章表模型
    
    Attributes:
        id: 主键
        title: 文章标题
        content: 文章内容（Markdown）
        summary: 文章摘要
        cover_image: 封面图 URL
        status: 文章状态
        view_count: 浏览量
        user_id: 作者 ID
        category_id: 分类 ID
        created_at: 创建时间
        updated_at: 更新时间
    """
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False, comment="文章标题")
    content = Column(Text, nullable=False, comment="文章内容")
    summary = Column(String(500), nullable=True, comment="文章摘要")
    cover_image = Column(String(255), nullable=True, comment="封面图URL")
    status = Column(Enum(ArticleStatus), default=ArticleStatus.draft, nullable=False, comment="文章状态")
    view_count = Column(Integer, default=0, nullable=False, comment="浏览量")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="作者ID")
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, comment="分类ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    author = relationship("User", back_populates="articles")
    category = relationship("Category", back_populates="articles")
    tags = relationship("Tag", secondary=article_tags, back_populates="articles")
