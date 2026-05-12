# -*- coding:utf-8 -*-
"""
@Time : 2022/4/27 5:24 PM
@Author: binkuolo
@Des: 用户管理
"""
import json
from core.Response import success, fail
from schemas.user import CreateUser, AccountLogin, UserInfo
from core.Utils import en_password, check_password
from core.Auth import create_access_token
from fastapi import Request
from fastapi.responses import JSONResponse
from DAL.Base import User_DA   # 只导入 User_DA
import asyncio

async def user_info(req: Request):
    """
    获取当前登陆用户信息(自我查询)
    """
    r = req.app.state.cache
    user_da = User_DA()

    #开启check_permissions后给出req.state.user_id
    user_id = req.state.user_id
    cache_key = f"user:{user_id}"

    cached_task = r.get(cache_key)
    db_task = asyncio.to_thread(user_da.get_by_id, user_id)

    cached, user_data = await asyncio.gather(cached_task, db_task)

    if cached:
        return success(msg="用户信息(缓存)",data = json.loads(cached))
    
    #缓存未命中后
    if not user_data:
        return fail(msg=f"用户ID{req.state.user_id}不存在!")
    
    #UserInfo是pydantic模型，过滤后创建对象
    user_info = UserInfo(**user_data.__dict__)
    user_info_dict = user_info.model_dump()

    # 写入缓存
    await r.setex(cache_key, 300, json.dumps(user_info_dict))

    return success(msg="用户信息", data=user_info_dict)


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
    return JSONResponse(
    status_code=201,
    content={"code": 201, "message": f"用户{create_user.username}创建成功", "data": {"id": create_user.id}}
)


def user_del(user_id: int):
    """
    删除用户
    """
    user_da = User_DA()
    deleted = user_da.delete(user_id)
    if not deleted:
        return fail(msg=f"用户{user_id}删除失败!")
    return JSONResponse(status_code=204, content=None)

async def account_login(post: AccountLogin, req: Request):
    r = req.app.state.cache

    username = post.username
    fail_key = f"login:fail:{username}"
    
    #检查是否已锁定
    fail_count = await r.get(fail_key)
    if fail_count and int(fail_count) >= 5:
        ttl = await r.ttl(fail_key)
        return fail(msg=f"账号已锁定，{ttl}秒后重试")
    
    #查询用户
    user_da = User_DA()
    get_user = user_da.get_by_username(username)
    
    #用户不存在
    if not get_user:
        new_count = await r.incr(fail_key)#初始创建1或增加1后返回值
        if new_count == 1:
            await r.expire(fail_key, 600)
        if new_count >= 5:
            await r.expire(fail_key, 600)
            return fail(msg="密码错误次数超过5次，账号已锁定10分钟")
        return fail(msg=f"用户名或密码错误，已失败{new_count}次")
    
    #管理员禁用
    if get_user.user_status != 1:  # 假设 1=正常，0=未激活，2=禁用
        return fail(msg=f"用户{username}已被管理员禁用")
    
    #密码错误
    if not check_password(post.password, get_user.password):
        new_count = await r.incr(fail_key)
        #第一次登录失败
        if new_count == 1:
            await r.expire(fail_key, 600)
        #第五次登录失败
        if new_count >= 5:
            await r.expire(fail_key, 600)
            return fail(msg="密码错误次数过多，账号已锁定10分钟")
        return fail(msg=f"用户名或密码错误，已失败{new_count}次")
    
    #登录成功
    await r.delete(fail_key)
    jwt_data = {
        "user_id": get_user.id,      # 注意：原Tortoise用pk，SQLAlchemy用id
        "user_type": get_user.user_type
    }
    jwt_token = create_access_token(data=jwt_data)
    return JSONResponse(
        {"code": 200, "message": "登陆成功😄", "data": {}},
        status_code=200,
        headers={"Set-Cookie": "X-token=Bearer " + jwt_token}
    )