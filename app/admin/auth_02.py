from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.exceptions import IncorrectEmailOrPasswordException
from app.auth import create_access_token, verify_password
from app.crud.user import user_crud
from app.core.db import async_session_manager


class AdminAuth(AuthenticationBackend):
    async def login(
        self,
        request: Request,
    ) -> bool:
        async with async_session_manager() as session:
            form = await request.form()
            username, password = form["username"], form["password"]
            user = await user_crud.find_one_or_none(session=session, name=username)
            if user is None:
                raise IncorrectEmailOrPasswordException
            verify = verify_password(
                plain_password=password, hashed_password=user.password
            )
            if not user or verify is False:
                return False
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
            return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key=settings.secret)
