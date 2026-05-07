from database.SA import get_sessionmaker
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from models.SA.Base import User, Role, Access

SessionLocal = get_sessionmaker()

class User_DA:
    def get_by_id(self, user_id: int):
        with SessionLocal() as session:
            result = session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()

    def get_by_username(self, username: str):
        with SessionLocal() as session:
            result = session.execute(select(User).where(User.username == username))
            return result.scalar_one_or_none()

    def get_list(self, skip: int = 0, limit: int = 100):
        with SessionLocal() as session:
            result = session.execute(select(User).offset(skip).limit(limit))
            return result.scalars().all()

    def create(self, **user_data):
        with SessionLocal() as session:
            user = User(**user_data)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def update(self, user_id: int, **update_data):
        with SessionLocal() as session:
            session.execute(update(User).where(User.id == user_id).values(**update_data))
            session.commit()
            return self.get_by_id(user_id)

    def delete(self, user_id: int):
        with SessionLocal() as session:
            result = session.execute(delete(User).where(User.id == user_id))
            session.commit()
            return result.rowcount > 0

    def exists_by_username(self, username: str) -> bool:
        with SessionLocal() as session:
            result = session.execute(select(User.id).where(User.username == username))
            return result.scalar_one_or_none() is not None


class Role_DA:
    def get_by_user_id(self, user_id: int):
        with SessionLocal() as session:
            result = session.execute(
                select(Role).join(Role.users).where(User.id == user_id)
            )
            return result.scalars().all()

    def get_roles_with_accesses(self, user_id: int):
        with SessionLocal() as session:
            result = session.execute(
                select(Role)
                .options(selectinload(Role.accesses))
                .join(Role.users)
                .where(User.id == user_id)
            )
            return result.scalars().all()


class Access_DA:
    def get_by_scopes(self, scopes: list):
        with SessionLocal() as session:
            result = session.execute(
                select(Access).where(Access.scopes.in_(scopes), Access.is_check == True)
            )
            return result.scalars().all()

    def get_user_scopes(self, user_id: int):
        with SessionLocal() as session:
            result = session.execute(
                select(Access.scopes)
                .join(Access.roles)
                .join(Role.users)
                .where(User.id == user_id, Access.is_check == True, Role.role_status == True)
            )
            return result.scalars().all()

    def user_has_any_scope(self, user_id: int, required_scopes: set) -> bool:
        with SessionLocal() as session:
            result = session.execute(
                select(Access)
                .join(Access.roles)
                .join(Role.users)
                .where(
                    User.id == user_id,
                    Access.scopes.in_(required_scopes),
                    Access.is_check == True,
                    Role.role_status == True
                )
                .limit(1)
            )
            return result.scalar_one_or_none() is not None
