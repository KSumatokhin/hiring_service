from contextlib import asynccontextmanager

from fastapi import FastAPI

# from sqladmin import Admin

# from app.admin.admin import KeywordAdmin, StopwordAdmin, UserAdmin
from app.api.routers import main_router
from app.core.config import config

# from app.core.db import engine
from app.core.init_db import create_first_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_first_superuser()
    yield


app = FastAPI(
    title=config.app.title,
    description=config.app.description,
    lifespan=lifespan,
)

app.include_router(main_router)
# admin = Admin(app, engine)

# admin.add_view(UserAdmin)
# admin.add_view(KeywordAdmin)
# admin.add_view(StopwordAdmin)
