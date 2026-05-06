#把py文件的运行目录放在pytest启动目录
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
import pytest

from sqlalchemy.ext.asyncio import create_async_engine
#切换至fake数据库
from database import SA
db_url = "mysql+aiomysql://root:123456@localhost:5000/test_db"
SA.engine = create_async_engine(db_url, echo=True)
from DAL.SA import AsyncSessionLocal


from app import application

from fastapi.testclient import TestClient
from models.SA.Base import User
from core.Utils import en_password
from sqlalchemy import delete
import asyncio

@pytest.fixture
def client():
    with TestClient(application) as c:
        yield c