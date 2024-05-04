from aiogram import Router

from .menu import menu_router
from .post import post_router
from .settings import settings_router
from .admin import admin_router

router = Router()
router.include_router(menu_router)
router.include_router(post_router)
router.include_router(settings_router)
router.include_router(admin_router)
