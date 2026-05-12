# FastAPI 权限系统

基于FastAPI+SQLAlchemy+Redis的RBAC后台管理系统。

## 认证方式

- 网页端：Session/Cookie
- API 端：JWT Token

## 核心功能

- JWT 登录认证
- RBAC 接口权限控制
- Redis 用户信息缓存
- 登录失败 5 次自动锁定
- 用户增删改查

## 技术栈

FastAPI / SQLAlchemy / MySQL / Redis / JWT / Pytest
