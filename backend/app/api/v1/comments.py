"""
评论相关 API
- 评论 CRUD
"""

from math import ceil
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.article import Article
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentResponse, CommentListResponse


router = APIRouter(tags=["评论"])


@router.get("/articles/{article_id}/comments", response_model=CommentListResponse, summary="获取文章评论")
def get_article_comments(
    article_id: int,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
):
    """
    获取文章的评论列表
    """
    # 检查文章是否存在
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    query = db.query(Comment).options(
        joinedload(Comment.user)
    ).filter(Comment.article_id == article_id)
    
    total = query.count()
    total_pages = ceil(total / page_size)
    
    comments = query.order_by(Comment.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return CommentListResponse(
        items=[CommentResponse.model_validate(c) for c in comments],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.post("/articles/{article_id}/comments", response_model=CommentResponse, summary="添加评论")
def create_comment(
    article_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    添加评论
    
    需要登录
    """
    # 检查文章是否存在
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在",
        )
    
    comment = Comment(
        content=comment_in.content,
        article_id=article_id,
        user_id=current_user.id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    # 加载用户信息
    comment = db.query(Comment).options(joinedload(Comment.user)).filter(Comment.id == comment.id).first()
    
    return comment


@router.delete("/comments/{comment_id}", summary="删除评论")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除评论
    
    评论作者、文章作者、管理员可删除
    """
    comment = db.query(Comment).options(
        joinedload(Comment.article)
    ).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在",
        )
    
    # 权限检查：评论作者、文章作者、管理员可删除
    is_comment_author = current_user.id == comment.user_id
    is_article_author = current_user.id == comment.article.user_id
    is_admin = current_user.role == "admin"
    
    if not (is_comment_author or is_article_author or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此评论",
        )
    
    db.delete(comment)
    db.commit()
    
    return {"message": "评论已删除"}
