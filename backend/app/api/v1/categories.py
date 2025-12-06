"""
分类相关 API
- 分类 CRUD
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db, get_current_user, get_current_user_optional
from app.models.user import User
from app.models.category import Category
from app.models.article import Article
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse


router = APIRouter(prefix="/categories", tags=["分类"])


@router.get("", response_model=List[CategoryResponse], summary="获取分类列表")
def get_categories(
    user_id: Optional[int] = Query(None, description="用户ID，筛选指定用户的分类"),
    db: Session = Depends(get_db),
):
    """
    获取分类列表
    
    支持按用户ID筛选，包含每个分类下的文章数量
    """
    # 查询分类及其文章数量
    query = db.query(Category)
    
    # 按用户筛选
    if user_id:
        query = query.filter(Category.user_id == user_id)
    
    categories = query.all()
    
    result = []
    for category in categories:
        # 统计文章数量
        article_count = db.query(func.count(Article.id)).filter(
            Article.category_id == category.id,
            Article.status == "published"
        ).scalar()
        
        category_response = CategoryResponse.model_validate(category)
        category_response.article_count = article_count
        result.append(category_response)
    
    return result


@router.get("/{category_id}", response_model=CategoryResponse, summary="获取分类详情")
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    获取分类详情
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在",
        )
    
    # 统计文章数量
    article_count = db.query(func.count(Article.id)).filter(
        Article.category_id == category.id,
        Article.status == "published"
    ).scalar()
    
    response = CategoryResponse.model_validate(category)
    response.article_count = article_count
    
    return response


@router.post("", response_model=CategoryResponse, summary="创建分类")
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建分类
    
    需要登录，分类将绑定到当前用户
    """
    # 检查当前用户下分类名是否已存在
    if db.query(Category).filter(
        Category.name == category_in.name,
        Category.user_id == current_user.id
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="分类名称已存在",
        )
    
    category = Category(
        name=category_in.name,
        description=category_in.description,
        user_id=current_user.id,  # 绑定当前用户
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    
    response = CategoryResponse.model_validate(category)
    response.article_count = 0
    
    return response


@router.put("/{category_id}", response_model=CategoryResponse, summary="更新分类")
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新分类
    
    仅分类所有者或管理员可更新
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在",
        )
    
    # 权限检查：仅所有者或管理员可更新
    if current_user.id != category.user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改此分类",
        )
    
    # 检查新名称是否与当前用户的其他分类冲突
    if category_in.name:
        existing = db.query(Category).filter(
            Category.name == category_in.name,
            Category.user_id == category.user_id,
            Category.id != category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="分类名称已存在",
            )
    
    update_data = category_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    # 统计文章数量
    article_count = db.query(func.count(Article.id)).filter(
        Article.category_id == category.id,
        Article.status == "published"
    ).scalar()
    
    response = CategoryResponse.model_validate(category)
    response.article_count = article_count
    
    return response


@router.delete("/{category_id}", summary="删除分类")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除分类
    
    仅分类所有者或管理员可删除
    删除分类后，该分类下的文章将变为无分类状态
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在",
        )
    
    # 权限检查：仅所有者或管理员可删除
    if current_user.id != category.user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此分类",
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "分类已删除"}
