from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

from models.SA.Base import Base
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



