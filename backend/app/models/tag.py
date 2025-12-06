"""
标签模型
"""

from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


# 文章-标签关联表（多对多）
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(Base):
    """
    标签表模型
    
    Attributes:
        id: 主键
        name: 标签名称
        user_id: 所属用户ID
    """
    __tablename__ = "tags"
    
    # 添加唯一约束：同一用户下标签名称唯一
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_tag_user_name'),
    )
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="标签名称")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="所属用户ID")
    
    # 关联关系（多对多）
    articles = relationship("Article", secondary=article_tags, back_populates="tags")
    user = relationship("User")
