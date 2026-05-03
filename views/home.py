# -*- coding:utf-8 -*-
"""
@Time : 2022/4/23 8:33 PM
@Author: binkuolo
@Des: views home
"""
from fastapi import Request, Form, Cookie
from typing import Optional
from DAL.SA import User_DA


async def home(request: Request, session_id: Optional[str] = Cookie(None)):
    cookie = session_id
    session = request.session.get("session")
    page_data = {
        "cookie": cookie,
        "session": session
    }
    return request.app.state.views.TemplateResponse("index.html", {"request": request, **page_data})


async def reg_page(req: Request):
    """
    注册页面
    :param req:
    :return: html
    """
    return req.app.state.views.TemplateResponse("reg_page.html", {"request": req})


async def result_page(req: Request, username: str = Form(...), password: str = Form(...)):
    """
    注册结果页面
    :param password: str
    :param username: str
    :param req:
    :return: html
    """
    user_da = User_DA()
    add_user = await user_da.create(username=username, password=password)
    print("插入的自增ID", add_user.id)
    print("插入的用户名", add_user.username)

    user_list = await user_da.get_list()
    for user in user_list:
        print(f"用户:{user.username}", user)

    get_user = await user_da.get_by_username(username)
    if not get_user:
        print("")
        return {"info": "没有查询到用户"}

    return req.app.state.views.TemplateResponse(
        "reg_result.html", {"request": req, "username": get_user.username, "password": get_user.password})