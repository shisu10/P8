# insert_test_data.py
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from models.SA.Base import User
from core.Utils import en_password
from sqlalchemy import delete
from database.SA import get_sessionmaker  # 根据你的实际路径调整
from sqlalchemy.ext.asyncio import create_async_engine
#切换至fake数据库
from database import SA
db_url = "mysql+aiomysql://root:123456@localhost:5000/test_db"
SA.engine = create_async_engine(db_url, echo=True)
from DAL.SA import AsyncSessionLocal

AsyncSessionLocal = get_sessionmaker()

async def insert_users():
    users_data = [
        ("admin", "12345678", 1),
        ("testuser1", "11111111", 1),
        ("testuser2", "22222222", 0),
    ]
    
    async with AsyncSessionLocal() as session:
        # 清除旧数据（可选）
        for username, _, _ in users_data:
            await session.execute(delete(User).where(User.username == username))
        
        # 插入新数据
        for username, password, status in users_data:
            user = User(
                username=username,
                password=en_password(password),
                user_status=status
            )
            session.add(user)
        
        await session.commit()
        print("测试数据插入成功！")

if __name__ == "__main__":
    asyncio.run(insert_users())