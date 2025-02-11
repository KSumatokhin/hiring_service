from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.core.config import settings
from app.exceptions import IncorrectEmailOrPasswordException
from app.auth import create_access_token, verify_password
from app.users.dao import UsersDAO


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        user = await UsersDAO.find_one_or_none(first_name=username)
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


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
