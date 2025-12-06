"""
管理员相关 API
- 统计数据
- 用户管理
- 评论管理
"""

from math import ceil
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.api.deps import get_db, get_current_admin_user
from app.models.user import User, UserRole
from app.models.article import Article
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.common import Statistics


router = APIRouter(prefix="/admin", tags=["管理员"])


@router.get("/statistics", response_model=Statistics, summary="获取统计数据")
def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    获取系统统计数据（管理员）
    """
    user_count = db.query(func.count(User.id)).scalar()
    article_count = db.query(func.count(Article.id)).scalar()
    view_count = db.query(func.sum(Article.view_count)).scalar() or 0
    
    return Statistics(
        user_count=user_count,
        article_count=article_count,
        view_count=view_count,
    )


@router.get("/users", summary="获取用户列表")
def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    获取用户列表（管理员）
    """
    query = db.query(User)
    
    total = query.count()
    total_pages = ceil(total / page_size)
    
    users = query.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "items": [UserResponse.model_validate(u) for u in users],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@router.put("/users/{user_id}", response_model=UserResponse, summary="更新用户")
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    更新用户信息（管理员）
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    update_data = user_in.model_dump(exclude_unset=True)
    
    # 检查用户名是否冲突
    if "username" in update_data:
        existing = db.query(User).filter(
            User.username == update_data["username"],
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已被使用",
            )
    
    # 检查邮箱是否冲突
    if "email" in update_data:
        existing = db.query(User).filter(
            User.email == update_data["email"],
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被使用",
            )
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/users/{user_id}", summary="删除用户")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    删除用户（管理员）
    
    不能删除自己
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除自己的账户",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "用户已删除"}

