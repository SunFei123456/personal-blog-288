"""
标签相关 API
- 标签 CRUD
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db, get_current_user, get_current_admin_user
from app.models.user import User
from app.models.tag import Tag, article_tags
from app.schemas.tag import TagCreate, TagResponse


router = APIRouter(prefix="/tags", tags=["标签"])


@router.get("", response_model=List[TagResponse], summary="获取标签列表")
def get_tags(db: Session = Depends(get_db)):
    """
    获取所有标签列表
    
    包含每个标签关联的文章数量
    """
    tags = db.query(Tag).all()
    
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
    
    需要登录
    """
    # 检查标签名是否已存在
    if db.query(Tag).filter(Tag.name == tag_in.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="标签名称已存在",
        )
    
    tag = Tag(name=tag_in.name)
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
    current_user: User = Depends(get_current_admin_user),
):
    """
    删除标签（管理员）
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在",
        )
    
    db.delete(tag)
    db.commit()
    
    return {"message": "标签已删除"}
