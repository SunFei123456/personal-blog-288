"""
分类模型
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Category(Base):
    """
    分类表模型
    
    Attributes:
        id: 主键
        name: 分类名称
        description: 分类描述
        created_at: 创建时间
    """
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, comment="分类名称")
    description = Column(String(255), nullable=True, comment="分类描述")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    # 关联关系
    articles = relationship("Article", back_populates="category")
