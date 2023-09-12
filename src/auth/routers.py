import fastapi.security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.password import PasswordHelper
from httpx import Request
from passlib.context import CryptContext
from sqlalchemy import update

from src.auth.base_config import current_user
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import VerifiedEmailCode, UserRead, ChangePassword
from src.database import get_async_session

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession


router_user = APIRouter(
    prefix='/user',
    tags=['User']
)

@router_user.post('/veridied')
async def email_verify(body: VerifiedEmailCode, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    print(body.code)
    print(user)
    if user.code == body.code:
        stmt = update(User).where(User.email == user.email).values(is_verified=True, code=None)
        print(stmt)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    else:
        return {"error": "Incorrect code"}


@router_user.get('/account', response_model=UserRead)
async def account_details(user: User = Depends(current_user)):
    return user


@router_user.post('/change-password')
async def change_password(body: ChangePassword, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session), user_manager=Depends(get_user_manager)):
    if body.old_password == body.new_password:
        raise HTTPException(status_code=400, detail='Passwords may not be repeated')
    verified, updated_password_hash = user_manager.password_helper.verify_and_update(body.old_password, user.hashed_password)
    if verified:
        stmt = update(User).where(User.email == user.email).values(hashed_password=user_manager.password_helper.hash(body.new_password))
        await session.execute(stmt)
        await session.commit()
    else:
        raise HTTPException(status_code=400, detail='You entered the wrong password')
    return {'status': 'Password updated successfully'}
#
# @router.get()
# async def reset_password():
#     pass
#
# @router.get()
# async def change_email():
#     pass
#
#
# @router.get()
# async def new_email_confirm():
#     pass
