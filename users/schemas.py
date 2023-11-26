from __future__ import annotations

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str
    name: str
    password: str


class UserLoginSchema(BaseModel):
    success: bool = False
    message: str = "Неверный логин или пароль"
