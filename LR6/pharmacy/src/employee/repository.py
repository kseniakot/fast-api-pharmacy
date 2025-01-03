from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.utils.base_repository import BaseRepository
from src.models import Employee, Role


class EmployeeRepository(BaseRepository):
    __tablename__ = "employee"

    @classmethod
    async def to_employee_object(cls, session, row):
        return Employee(
            id=row[0],
            role=await RoleRepository.find_one_or_none(session, row[1]),
            first_name=row[2],
            last_name=row[3],
            phone=row[4],
            email=row[5],
            password=row[6]
        )

    @classmethod
    async def find_one_or_none_by_email(cls, session: AsyncSession, email: str):
        query = text(f"SELECT * FROM {cls.__tablename__} WHERE email = :email")
        try:
            result = await cls.execute_raw_sql(session, query, {"email": email}, fetch_one=True)
            if result:
                return await cls.to_employee_object(session, result)
        except SQLAlchemyError as e:
            print(f"Error finding one by email: {e}")
            return None

    @classmethod
    async def add_one(cls, session: AsyncSession, values: dict):
        role = await RoleRepository.find_one_by_name(session, values.get("role_id"))
        if not role:
            raise ValueError("Role not found")
        values["role_id"] = role.id
        row = (await super().add_one(session, values))
        if row:
            return await cls.to_employee_object(session, row)

    @classmethod
    async def update_one(cls, session: AsyncSession, id: int, values: dict):
        role = await RoleRepository.find_one_by_name(session, values.get("role_id"))
        if not role:
            raise ValueError("Role not found")
        values["role_id"] = role.id
        row = (await super().update_one(session, id, values))
        if row:
            return await cls.to_employee_object(session, row)

    @classmethod
    async def find_all(cls, session: AsyncSession):
        query = text("SELECT * FROM employee JOIN role ON employee.role_id = role.id")
        rows = (await session.execute(query)).fetchall()
        employees = []
        for row in rows:
            role = Role(id=row[7], name=row[8], description=row[9])
            employee = Employee(
                id=row[0],
                role=role,
                first_name=row[2],
                last_name=row[3],
                phone=row[4],
                email=row[5],
                password=row[6]
            )
            employees.append(employee)
        return employees

    @classmethod
    async def delete_one(cls, session: AsyncSession, id: int):
        row = (await super().delete_one(session, id))
        if row:
            return await cls.to_employee_object(session, row)

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, id: int):
        row = (await super().find_one_or_none(session, id))
        if row:
            return await cls.to_employee_object(session, row)


class RoleRepository(BaseRepository):
    __tablename__ = "role"

    @classmethod
    def to_role_object(cls, row):
        return Role(
            id=row[0],
            name=row[1],
            description=row[2]
        )

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, id: int):
        row = (await super().find_one_or_none(session, id))
        if row:
            return cls.to_role_object(row)

    @classmethod
    async def add_one(cls, session: AsyncSession, values: dict):
        row = (await super().add_one(session, values))
        if row:
            return cls.to_role_object(row)

    @classmethod
    async def find_one_by_name(cls, session: AsyncSession, name: str):
        query = text(f"SELECT * FROM {cls.__tablename__} WHERE name = :name")
        try:
            result = await cls.execute_raw_sql(session, query, {"name": name}, fetch_one=True)
            if result:
                return cls.to_role_object(result)
        except SQLAlchemyError as e:
            print(f"Error finding one by name: {e}")
