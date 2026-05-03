from database.SA import SessionLocal
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from models.SA.Base import User, Role, Access


class User_DA:
    async def get_by_id(self, user_id: int):
        async with SessionLocal() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()

    async def get_by_username(self, username: str):
        async with SessionLocal() as session:
            result = await session.execute(select(User).where(User.username == username))
            return result.scalar_one_or_none()

    async def get_list(self, skip: int = 0, limit: int = 100):
        async with SessionLocal() as session:
            result = await session.execute(select(User).offset(skip).limit(limit))
            return result.scalars().all()

    async def create(self, **user_data):
        async with SessionLocal() as session:
            user = User(**user_data)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def update(self, user_id: int, **update_data):
        async with SessionLocal() as session:
            await session.execute(update(User).where(User.id == user_id).values(**update_data))
            await session.commit()
            return await self.get_by_id(user_id)

    async def delete(self, user_id: int):
        async with SessionLocal() as session:
            await session.execute(delete(User).where(User.id == user_id))
            await session.commit()
            return True

    async def exists_by_username(self, username: str) -> bool:
        async with SessionLocal() as session:
            result = await session.execute(select(User.id).where(User.username == username))
            return result.scalar_one_or_none() is not None
  

class Role_DA:
    async def get_by_user_id(self, user_id: int):
        async with SessionLocal() as session:
            result = await session.execute(
                select(Role).join(Role.user).where(User.id == user_id)
            )
            return result.scalars().all()

    async def get_roles_with_accesses(self, user_id: int):
        async with SessionLocal() as session:
            result = await session.execute(
                select(Role)
                .options(selectinload(Role.access))
                .join(Role.user)
                .where(User.id == user_id)
            )
            return result.scalars().all()


class Access_DA:
    async def get_by_scopes(self, scopes: list):
        async with SessionLocal() as session:
            result = await session.execute(
                select(Access).where(Access.scopes.in_(scopes), Access.is_check == True)
            )
            return result.scalars().all()

    async def get_user_scopes(self, user_id: int):
        async with SessionLocal() as session:
            result = await session.execute(
                select(Access.scopes)
                .join(Access.role)
                .join(Role.user)
                .where(User.id == user_id, Access.is_check == True, Role.role_status == True)
            )
            return result.scalars().all()
