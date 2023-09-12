from smtplib import SMTPDataError, SMTPRecipientsRefused
from typing import Optional

from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from src.auth.models import User
from src.auth.task import send_email_report_dashboard
from src.auth.utils import get_user_db, generated_code

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    # async def hashed_password(self, password):
    #     hash_password = self.password_helper.hash(password)
    #     return hash_password

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["code"] = int(generated_code())
        try:
            send_email_report_dashboard(username=user_dict['username'], email=user_dict['email'], code=user_dict["code"])
        except (SMTPDataError, SMTPRecipientsRefused):
            raise HTTPException(status_code=400, detail={'error': "Email verification failed"})

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)