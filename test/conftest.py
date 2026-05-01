#把py文件的运行目录放在pytest启动目录
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise

# 1. 阻止 app 启动时连真实数据库
from database import mysql
async def fake_register(app):
    pass
mysql.register_mysql = fake_register

# 2. 现在导入 app（startup 会调用 fake_register，什么都不做）
from app import application
from models.base import User
from core.Utils import en_password

@pytest.fixture
def client():
    with TestClient(application) as c:
        import asyncio
        
        # 3. 手动连内存数据库（必须用 config 格式，不能只用 db_url）
        async def setup():
            await Tortoise.init(config={
                "connections": {"base": "sqlite://:memory:"},
                "apps": {
                    "base": {
                        "models": ["models.base"],
                        "default_connection": "base"
                    }
                },
                'use_tz': False,
                'timezone': 'Asia/Shanghai'
            })
            await Tortoise.generate_schemas()  # 建表
            # 插测试用户
            await User.create(
                username="admin",
                password=en_password("12345678"),
                user_status=1
            )
        
        asyncio.run(setup())
        yield c
        asyncio.run(Tortoise.close_connections())