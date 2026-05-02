import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/test_db",
    echo=True,  #打印SQL日志
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



