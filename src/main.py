from fastapi import FastAPI, Depends

from src.auth.base_config import fastapi_users, auth_backend
from src.auth.routers import router_user
from src.auth.schemas import UserRead, UserCreate
from src.backend.routers import router as router_shop


app = FastAPI(title='FirstProject')

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["JWT auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["User"],
)

app.include_router(router_shop)
app.include_router(router_user)
