from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)

def get_sessionmaker():
    SessionLocal = sessionmaker(engine, expire_on_commit=False)
    return SessionLocal

# 没有表创建表
# from models.SA.Base import Base
# def init_db():
#     with engine.begin() as conn:
#         conn.run_sync(Base.metadata.create_all)


