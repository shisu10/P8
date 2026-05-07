# -*- coding:utf-8 -*-
"""
@Time : 2022/4/27 5:24 PM
@Author: binkuolo
@Des: 用户管理
"""
from core.Response import success, fail
from schemas.user import CreateUser, AccountLogin, UserInfo
from core.Utils import en_password, check_password
from core.Auth import create_access_token
from fastapi import Request
from fastapi.responses import JSONResponse
from DAL.Base import User_DA   # 只导入 User_DA


def user_info(req: Request):
    """
    获取当前登陆用户信息
    """
    user_da = User_DA()
    user_data = user_da.get_by_id(req.state.user_id)
    if not user_data:
        return fail(msg=f"用户ID{req.state.user_id}不存在!")
    return success(msg="用户信息", data=UserInfo(**user_data.__dict__))


def user_add(post: CreateUser):
    """
    创建用户
    """
    user_da = User_DA()
    post.password = en_password(post.password)
    # 注意：post.dict() 只包含 username, password，没有 user_type
    create_user = user_da.create(**post.dict())
    if not create_user:
        return fail(msg=f"用户{post.username}创建失败!")
    return success(msg=f"用户{create_user.username}创建成功")


def user_del(user_id: int):
    """
    删除用户
    """
    user_da = User_DA()
    deleted = user_da.delete(user_id)
    if not deleted:
        return fail(msg=f"用户{user_id}删除失败!")
    return success(msg="删除成功")


def account_login(post: AccountLogin):
    """
    用户登陆
    """
    user_da = User_DA()
    get_user = user_da.get_by_username(post.username)
    if not get_user:
        return fail(msg=f"用户{post.username}密码验证失败!")
    if not check_password(post.password, get_user.password):
        return fail(msg=f"用户{post.username}密码验证失败!")
    if not get_user.user_status:
        return fail(msg=f"用户{post.username}已被管理员禁用!")
    jwt_data = {
        "user_id": get_user.id,      # 注意：原 Tortoise 用 pk，SQLAlchemy 用 id
        "user_type": get_user.user_type
    }
    jwt_token = create_access_token(data=jwt_data)
    return JSONResponse(
        {"code": 200, "message": "登陆成功😄", "data": {}},
        status_code=200,
        headers={"Set-Cookie": "X-token=Bearer " + jwt_token}
    )