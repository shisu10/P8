#把py文件的运行目录放在pytest启动目录
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine


#切换至fake数据库
from database import SA
db_url = "mysql+aiomysql://root:123456@localhost:5000/test_db"
SA.engine = create_async_engine(db_url, echo=True)
from DAL.SA import AsyncSessionLocal


from app import application
@pytest.fixture
def client():
    with TestClient(application) as c:
        import asyncio
        from models.SA.Base import User
        from core.Utils import en_password
        from sqlalchemy import delete
        
        # async def setup():
        #     async with AsyncSessionLocal() as session:
        #         # 准备测试数据（简单列表）
        #         users_data = [
        #             ("admin", "12345678", 1),
        #             ("testuser1", "11111111", 1),
        #             ("testuser2", "22222222", 0),
        #         ]
                
        #         # 删除已存在的
        #         for username, _, _ in users_data:
        #             await session.execute(delete(User).where(User.username == username))
                
        #         # 批量插入
        #         for username, password, status in users_data:
        #             user = User(username=username, password=en_password(password), user_status=status)
        #             session.add(user)
                
        #         await session.commit()
        
        # asyncio.run(setup())
        yield c
