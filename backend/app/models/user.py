"""
用户模型
"""

from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class UserRole(str, enum.Enum):
    """用户角色枚举"""
    user = "user"
    admin = "admin"


class User(Base):
    """
    用户表模型
    
    Attributes:
        id: 主键
        username: 用户名（唯一）
        email: 邮箱（唯一）
        password_hash: 密码哈希
        avatar: 头像 URL
        role: 用户角色
        created_at: 创建时间
        updated_at: 更新时间
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    avatar = Column(String(255), nullable=True, comment="头像URL")
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False, comment="用户角色")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    articles = relationship("Article", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
