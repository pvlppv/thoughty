from aiogram import types
from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hlink
from aiogram.types import Message
from bot.utils.logging import handler
from bot.filters.chat_type import ChatTypeFilter
from bot.utils.api_utils import methods
from bot.keyboards.inline import menu_inline_keyboard
from aiogram.fsm.context import FSMContext

menu_router = Router(name="menu")
menu_router.message.filter(ChatTypeFilter(chat_type=["private"]))


@menu_router.message(CommandStart())
async def start_handler(message: Message):
    handler(__name__, type=message)
    await methods.create_user(telegram_id=message.from_user.id)
    await message.answer(
        text=
        f"Привет, Соти - это {hlink('социальный дневник чувств', 'https://t.me/thoughty_channel')} для Вышкинцев, "
        "проще говоря: лента-отдушина, где каждый может быть услышан.\n\n"
        "В этом боте ты взаимодействуешь с этой лентой: создаёшь свои сообщения, отвечаешь на чужие, смотришь статистику и так далее.\n"
        "Здесь всё анонимно, в базе данных мы храним только твой телеграм айди, поэтому и регистрации никакой нет, собственно всё :)\n\n"
        "Кликай в меню ниже:",
        reply_markup=menu_inline_keyboard(),
    )


@menu_router.callback_query(F.data == "menu")
async def menu_handler_callback(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    await callback.message.edit_text(
        text=
        f"Привет, Соти - это {hlink('социальный дневник чувств', 'https://t.me/thoughty_channel')} для Вышкинцев, "
        "проще говоря: лента-отдушина, где каждый может быть услышан.\n\n"
        "В этом боте ты взаимодействуешь с этой лентой: создаёшь свои сообщения, отвечаешь на чужие, смотришь статистику и так далее.\n"
        "Здесь всё анонимно, в базе данных мы храним только твой телеграм айди, поэтому и регистрации никакой нет, собственно всё :)\n\n"
        "Кликай в меню ниже:",
        reply_markup=menu_inline_keyboard(),
    )
    await state.clear()
