from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import (
    UserUpdate,
    UserCreate,
    AdminCreate,
)


class CRUDUser(CRUDBase):
    pass


user_crud = CRUDUser(User)
