# -*- coding:utf-8 -*-
"""
@Time : 2022/4/27 3:40 PM
@Author: binkuolo
@Des: JWT鉴权
"""
from datetime import timedelta, datetime
import jwt
from fastapi import HTTPException, Request, Depends
from fastapi.security import SecurityScopes
from fastapi.security.oauth2 import get_authorization_scheme_param, OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError
from starlette import status
from config import settings
from DAL.SA import User_DA, Access_DA

OAuth2 = OAuth2PasswordBearer("")


def create_access_token(data: dict):
    """
    创建token
    :param data: 加密数据
    :return: jwt
    """
    token_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data.update({"exp": expire})
    jwt_token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return jwt_token


async def check_permissions(req: Request, security_scopes: SecurityScopes, token=Depends(OAuth2)):
    """
    权限验证
    :param token:
    :param req:
    :param security_scopes: 权限域
    :return:
    """
    print("token", token)
    print("scopes", security_scopes.scopes)
    authorization: str = req.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)

    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = param
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        if payload:
            user_id = payload.get("user_id", None)
            user_type = payload.get("user_type", None)
            if user_id is None or user_type is None:
                credentials_exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="无效凭证",
                    headers={"WWW-Authenticate": f"Bearer{token}"},
                )
                raise credentials_exception
        else:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效凭证",
                headers={"WWW-Authenticate": f"Bearer {token}"},
            )
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="凭证已证过期",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    except (PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )

    user_da = User_DA()
    check_user = await user_da.get_by_id(user_id)
    if not check_user or check_user.user_status != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已经被管理员禁用!",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )

    if security_scopes.scopes:
        print("当前域：", security_scopes.scopes)
        scopes = []
        if not user_type and security_scopes.scopes:
            access_da = Access_DA()
            has_permission = await access_da.user_has_any_scope(user_id, set(security_scopes.scopes))
            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not permissions",
                    headers={"scopes": security_scopes.scope_str},
                )
            scopes = await access_da.get_user_scopes(user_id)
        req.state.scopes = scopes

    req.state.user_id = user_id
    req.state.user_type = user_type
