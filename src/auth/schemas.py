from enum import Enum
from typing import Optional

from fastapi import HTTPException
from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, field_validator


class UserType(str, Enum):
    shop = 'shop'
    buyer = 'buyer'


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    type: UserType

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    type: Optional[UserType] = 'buyer'

    @field_validator('password')
    def validate_password(cls, value):
        if len(value) < 6:
            raise HTTPException(status_code=400, detail={"error": "The password must be 6 or more characters long."})
        else:
            return value


class VerifiedEmailCode(BaseModel):
    code: int

    @field_validator("code")
    def validate_code(cls, value):
        if not int(value) > 4 or int(value) < 4:
            raise HTTPException(status_code=400, detail={"error": "Code must be 4 digits"})
        else:
            return value

    class Config:
        orm_mode = True


class ChangePassword(BaseModel):
    old_password: str
    new_password: str






