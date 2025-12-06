"""
分类模型
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
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
        user_id: 所属用户ID
        created_at: 创建时间
    """
    __tablename__ = "categories"
    
    # 添加唯一约束：同一用户下分类名称唯一
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_category_user_name'),
    )
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="分类名称")
    description = Column(String(255), nullable=True, comment="分类描述")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="所属用户ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    # 关联关系
    articles = relationship("Article", back_populates="category")
    user = relationship("User")
