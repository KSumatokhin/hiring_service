import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

import logging


# from sqladmin import Admin, ModelView
from sqladmin import Admin
from telegram import Update

from app.api.routers import main_router

# from app.auth import get_password_hash
from app.admin.auth import AdminAuth
from app.bot.bot import application
from app.core.config import settings
from app.core.db import engine
from app.core.init_db import create_first_admin

from app.admin import UserAdmin, KeywordAdmin, StopwordAdmin

# from app.admin.auth import authentication_backend

logger = logging.getLogger(__name__)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info("Starting Telegram bot...")
#     bot_task = asyncio.create_task(run_bot())
#     yield
#     logger.info("Stopping Telegram bot...")
#     bot_task.cancel()
#     try:
#         await bot_task
#     except asyncio.CancelledError:
#         logger.info("Telegram bot stopped.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Telegram bot...")
    await application.initialize()
    await application.start()
    logger.info("listening for new messages...")
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

    yield

    logger.info("Telegram bot stopped.")
    await application.updater.stop()
    await application.stop()
    await application.shutdown()


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan,
)


app.include_router(main_router)


admin = Admin(app, engine, authentication_backend=AdminAuth())
admin.add_view(UserAdmin)
admin.add_view(KeywordAdmin)
admin.add_view(StopwordAdmin)

# uvicorn app.main:app --reload
