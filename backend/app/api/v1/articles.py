"""
文章相关 API
- 文章 CRUD
- 文章列表查询
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from math import ceil
from app.api.deps import get_db, get_current_user, get_current_user_optional
from app.models.user import User
from app.models.article import Article, ArticleStatus
from app.models.category import Category
from app.models.tag import Tag
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse


router = APIRouter(prefix="/articles", tags=["文章"])


@router.get("", response_model=ArticleListResponse, summary="获取文章列表")
def get_articles(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[ArticleStatus] = Query(None, description="文章状态"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    tag_id: Optional[int] = Query(None, description="标签ID"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    user_id: Optional[int] = Query(None, description="作者ID"),
    db: Session = Depends(get_db),
):
    """
    获取文章列表（分页）
    
    支持按状态、分类、标签、关键词筛选
    """
    query = db.query(Article).options(
        joinedload(Article.author),
        joinedload(Article.category),
        joinedload(Article.tags),
    )
    
    # 筛选条件
    if status:
        query = query.filter(Article.status == status)
    if category_id:
        query = query.filter(Article.category_id == category_id)
    if tag_id:
        query = query.join(Article.tags).filter(Tag.id == tag_id)
    if keyword:
        query = query.filter(Article.title.contains(keyword))
    if user_id:
        query = query.filter(Article.user_id == user_id)
    
    # 计算总数
    total = query.count()
    total_pages = ceil(total / page_size)
    
    # 分页查询
    articles = query.order_by(Article.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return ArticleListResponse(
        items=[ArticleResponse.model_validate(a) for a in articles],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/my", response_model=ArticleListResponse, summary="获取我的文章列表")
def get_my_articles(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[ArticleStatus] = Query(None, description="文章状态"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取当前用户的文章列表
    """
    query = db.query(Article).options(
        joinedload(Article.author),
        joinedload(Article.category),
        joinedload(Article.tags),
    ).filter(Article.user_id == current_user.id)
    
    if status:
        query = query.filter(Article.status == status)
    
    total = query.count()
    total_pages = ceil(total / page_size)
    
    articles = query.order_by(Article.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return ArticleListResponse(
        items=[ArticleResponse.model_validate(a) for a in articles],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{article_id}", response_model=ArticleResponse, summary="获取文章详情")
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    获取文章详情
    
    - 已发布文章：所有人可查看
    - 草稿文章：仅作者和管理员可查看
    """
    article = db.query(Article).options(
        joinedload(Article.author),
        joinedload(Article.category),
        joinedload(Article.tags),
    ).filter(Article.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    # 草稿文章权限检查
    if article.status == ArticleStatus.draft:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在",
            )
        if current_user.id != article.user_id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在",
            )
    
    # 增加浏览量
    article.view_count += 1
    db.commit()
    db.refresh(article)
    
    return article


@router.post("", response_model=ArticleResponse, summary="创建文章")
def create_article(
    article_in: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建文章
    
    需要登录
    """
    # 验证分类是否存在
    if article_in.category_id:
        category = db.query(Category).filter(Category.id == article_in.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="分类不存在",
            )
    
    # 获取标签
    tags = []
    if article_in.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(article_in.tag_ids)).all()
    
    # 创建文章
    article = Article(
        title=article_in.title,
        content=article_in.content,
        summary=article_in.summary,
        cover_image=article_in.cover_image,
        status=article_in.status,
        category_id=article_in.category_id,
        user_id=current_user.id,
        tags=tags,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    
    return article


@router.put("/{article_id}", response_model=ArticleResponse, summary="更新文章")
def update_article(
    article_id: int,
    article_in: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新文章
    
    仅作者和管理员可更新
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    # 权限检查
    if current_user.id != article.user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改此文章",
        )
    
    # 更新字段
    update_data = article_in.model_dump(exclude_unset=True)
    
    # 处理标签
    if "tag_ids" in update_data:
        tag_ids = update_data.pop("tag_ids")
        if tag_ids is not None:
            tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
            article.tags = tags
    
    for field, value in update_data.items():
        setattr(article, field, value)
    
    db.commit()
    db.refresh(article)
    
    return article


@router.delete("/{article_id}", summary="删除文章")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除文章
    
    仅作者和管理员可删除
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    # 权限检查
    if current_user.id != article.user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此文章",
        )
    
    db.delete(article)
    db.commit()
    
    return {"message": "文章已删除"}
