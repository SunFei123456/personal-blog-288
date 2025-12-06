"""
API 依赖模块
- 数据库会话依赖
- 用户认证依赖
- 权限检查依赖
"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.core.security import decode_access_token
from app.models.user import User, UserRole


# HTTP Bearer 认证（配置为返回 401）
security = HTTPBearer(auto_error=False)


def get_credentials(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> HTTPAuthorizationCredentials:
    """
    获取认证凭证，未提供时返回 401
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials


def get_db() -> Generator:
    """
    获取数据库会话依赖
    
    Yields:
        数据库会话实例
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    获取当前登录用户依赖
    
    Args:
        credentials: HTTP Bearer 凭证
        db: 数据库会话
        
    Returns:
        当前用户对象
        
    Raises:
        HTTPException: 认证失败
    """
    # 检查是否提供了认证凭证
    if credentials is None:
        print("[AUTH DEBUG] No credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    print(f"[AUTH DEBUG] Token received: {token[:20]}..." if len(token) > 20 else f"[AUTH DEBUG] Token: {token}")
    payload = decode_access_token(token)
    print(f"[AUTH DEBUG] Payload: {payload}")
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 将字符串转换为整数
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的用户ID",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    获取当前用户（可选）依赖
    用于不强制要求登录的接口
    
    Args:
        credentials: HTTP Bearer 凭证（可选）
        db: 数据库会话
        
    Returns:
        当前用户对象或 None
    """
    if credentials is None:
        return None
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        return None
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        return None
    
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前管理员用户依赖
    
    Args:
        current_user: 当前用户
        
    Returns:
        管理员用户对象
        
    Raises:
        HTTPException: 权限不足
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限",
        )
    return current_user
