from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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


templates = Jinja2Templates(directory="app/templates")


@app.get(path="/admin/login", response_class=HTMLResponse)
async def login(request: Request):
    print("kaka")
    return templates.TemplateResponse("login.html", {"request": request})
