from aiogram import Router, types, exceptions
from aiogram.fsm.context import FSMContext
from loguru import logger

from .menu import menu_router
from .post import post_router
from .settings import settings_router
from .admin import admin_router

router = Router()
router.include_router(menu_router)
router.include_router(post_router)
router.include_router(settings_router)
router.include_router(admin_router)


@router.error()
async def error_handler(event: types.ErrorEvent, state: FSMContext):
    await state.clear()

    if event.update.callback_query:
        await event.update.callback_query.answer()
        user_id = event.update.callback_query.from_user.id
    else:
        user_id = event.update.message.from_user.id

    logger.critical(f'ERROR | User <{user_id}> | {type(event.exception)} | {event.exception}')
