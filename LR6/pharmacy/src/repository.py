from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.utils.base_repository import BaseRepository
from models import Client


class ClientRepository(BaseRepository):
    __tablename__ = "client"

    @classmethod
    def to_client_object(cls, row):
        return Client(
            id=row[0],
            first_name=row[1],
            last_name=row[2],
            date_of_birth=row[3],
            phone=row[4],
            email=row[5],
            password=row[6],
        )

    @classmethod
    async def find_one_or_none_by_email(cls, session: AsyncSession, email: str):
        row = (await super().find_one_or_none_by_email(session, email))
        if row:
            return cls.to_client_object(row)
        return None

    @classmethod
    async def add_one(cls, session: AsyncSession, values: dict):
        row = (await super().add_one(session, values))
        if row:
            return cls.to_client_object(row)
        return None