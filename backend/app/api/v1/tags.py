"""
标签相关 API
- 标签 CRUD
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.tag import Tag, article_tags
from app.schemas.tag import TagCreate, TagResponse


router = APIRouter(prefix="/tags", tags=["标签"])


@router.get("", response_model=List[TagResponse], summary="获取标签列表")
def get_tags(
    user_id: Optional[int] = Query(None, description="用户ID，筛选指定用户的标签"),
    db: Session = Depends(get_db),
):
    """
    获取标签列表
    
    支持按用户ID筛选，包含每个标签关联的文章数量
    """
    query = db.query(Tag)
    
    # 按用户筛选
    if user_id:
        query = query.filter(Tag.user_id == user_id)
    
    tags = query.all()
    
    result = []
    for tag in tags:
        # 统计文章数量
        article_count = db.query(func.count(article_tags.c.article_id)).filter(
            article_tags.c.tag_id == tag.id
        ).scalar()
        
        tag_response = TagResponse.model_validate(tag)
        tag_response.article_count = article_count
        result.append(tag_response)
    
    return result


@router.post("", response_model=TagResponse, summary="创建标签")
def create_tag(
    tag_in: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建标签
    
    需要登录，标签将绑定到当前用户
    """
    # 检查当前用户下标签名是否已存在
    if db.query(Tag).filter(
        Tag.name == tag_in.name,
        Tag.user_id == current_user.id
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="标签名称已存在",
        )
    
    tag = Tag(name=tag_in.name, user_id=current_user.id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    
    response = TagResponse.model_validate(tag)
    response.article_count = 0
    
    return response


@router.delete("/{tag_id}", summary="删除标签")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除标签
    
    仅标签所有者或管理员可删除
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在",
        )
    
    # 权限检查：仅所有者或管理员可删除
    if current_user.id != tag.user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此标签",
        )
    
    db.delete(tag)
    db.commit()
    
    return {"message": "标签已删除"}
