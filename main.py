from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger

import bot.routers
from backend_api.routers import routers
from backend_api.database import engine
from backend_api import models
from settings import get_settings

cfg = get_settings()


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("🚀 Starting application")
    from bot.bot import start_telegram
    await start_telegram()
    yield
    logger.info("⛔ Stopping application")

app = FastAPI(lifespan=lifespan)
# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
for router in routers:
    app.include_router(router)
