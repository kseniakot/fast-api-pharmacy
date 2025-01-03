from datetime import timedelta
from typing import Annotated

import jwt
from jwt import InvalidTokenError
from fastapi import APIRouter, HTTPException, status, Depends

from fastapi.security import OAuth2PasswordRequestForm  # standard FastAPI class for login form (username and password)

from src.utils.config import settings
from src.auth.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
)

from src.auth.schemas import SToken

from src.client.schemas import SClientAuth, SClientCreate
from src.client.service import ClientService
from src.employee.schemas import SEmployeeAuth
from src.employee.service import EmployeeService

auth_router = APIRouter(prefix="/users", tags=["Manage users"])


@auth_router.post("/token", response_model=SToken, description="Get access token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> SToken:
    client = await ClientService.get_client_by_email(form_data.username)
    employee = await EmployeeService.get_employee_by_email(form_data.username)

    if not client and not employee or client and not verify_password(form_data.password,
                                                                     client.password) or employee and not verify_password(
        form_data.password, employee.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = None
    refresh_token = None

    if client:
        access_token = create_access_token(
            data={"sub": client.email,
                  "id": client.id},

            user_role="client",
            expires_delta=access_token_expires,
        )
        refresh_token = create_access_token(
            data={"sub": client.email,
                  "id": client.id}, expires_delta=timedelta(days=180)
        )
    elif employee:
        access_token = create_access_token(
            data={"sub": employee.email,
                  "id": employee.id},
            user_role=employee.role.name,
            expires_delta=access_token_expires,
        )
        refresh_token = create_access_token(
            data={"sub": employee.email,
                  "id": employee.id}, expires_delta=timedelta(days=180)
        )

    return SToken(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@auth_router.post("/refresh")
async def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        client = await ClientService.get_client_by_email(email=username)
        employee = await EmployeeService.get_employee_by_email(email=username)

        if not client and not employee:
            raise HTTPException(status_code=401, detail="User not found")

        access_token = create_access_token(data={"sub": username,
                                                 "id": client.id if client else employee.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@auth_router.post("/register", response_model=SClientAuth, description="Register new user")
async def register_user(
        client_data: SClientCreate = Depends(), ) -> SClientAuth:
    client = await ClientService.get_client_by_email(email=client_data.email)
    if client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = get_password_hash(client_data.password)

    new_client_data = client_data.model_dump()
    print(new_client_data)
    new_client_data["password"] = hashed_password
    new_user = await ClientService.add_client(new_client_data)

    return SClientAuth.model_validate(new_user)
