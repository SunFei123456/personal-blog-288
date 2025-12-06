"""
认证相关 API
- 用户注册
- 用户登录
- 获取当前用户信息
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.security import verify_password, get_password_hash, create_access_token


router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=UserResponse, summary="用户注册")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    
    - **username**: 用户名（3-50字符，唯一）
    - **email**: 邮箱（唯一）
    - **password**: 密码（至少6字符）
    """
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被注册",
        )
    
    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册",
        )
    
    # 创建用户
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role=UserRole.user,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/login", response_model=Token, summary="用户登录")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录接口
    
    - **username**: 用户名
    - **password**: 密码
    
    返回 JWT Token 和用户信息
    """
    # 查找用户
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    
    # 验证密码
    if not verify_password(user_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    
    # 生成 Token（sub 必须是字符串）
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
def get_me(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户信息
    
    需要携带有效的 JWT Token
    """
    return current_user
