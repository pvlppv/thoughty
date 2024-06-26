from aiogram import types
from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.utils.markdown import hlink
from aiogram.types import Message
from bot.utils.logging import handler
from bot.filters.chat_type import ChatTypeFilter
from bot.utils.api_utils import methods
from bot.keyboards.inline import admin_inline_keyboard, menu_back_inline_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold, hitalic
from bot.loader import bot
from bot.utils.api_utils import methods
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
import re
from settings import get_settings

cfg = get_settings()

admin_router = Router(name="admin")
admin_router.message.filter(ChatTypeFilter(chat_type=["private"]))


class StateAdmin(StatesGroup):
    id = State()


@admin_router.message(Command("admin"))
async def admin_handler(message: Message):
    handler(__name__, type=message)
    user = await methods.get_user(tg_user_id=message.from_user.id)
    if user["role"] == "admin":
        await message.answer(f"{hbold('Админ-панель')}:", reply_markup=admin_inline_keyboard())


@admin_router.callback_query(F.data == "admin_delete_post")
async def admin_delete_post_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    await state.set_state(StateAdmin.id)
    await callback.answer()
    await callback.message.edit_text("Пришли ссылку на сообщение:", reply_markup=menu_back_inline_keyboard())
    await state.update_data({"type": "channel"})


@admin_router.callback_query(F.data == "admin_delete_answer")
async def admin_delete_answer_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    await state.set_state(StateAdmin.id)
    await callback.answer()
    await callback.message.edit_text("Пришли ссылку на ответ:", reply_markup=menu_back_inline_keyboard())
    await state.update_data({"type": "group"})


@admin_router.message(StateAdmin.id)
async def admin_id_handler(message: Message, state: FSMContext):
    handler(__name__, type=message)
    data = await state.get_data()
    match = re.search(r'/(\d+)$', message.text)
    if match:
        post_id = match.group(1)
    else:
        await message.answer("Неверный формат ссылки")
        return
    if data["type"] == "channel":
        post = await methods.get_post_by_tg_msg_channel_id(tg_msg_channel_id=post_id)
    elif data["type"] == "group":
        post = await methods.get_answer_by_tg_msg_ans_id(tg_msg_ans_id=post_id)
    if not post:
        await message.answer("Сообщение не найдено")
        return
    if data["type"] == "channel":
        await bot.delete_message(chat_id=f"{cfg.channel_id}", message_id=post["tg_msg_channel_id"])
        await methods.delete_post(tg_msg_channel_id=post["tg_msg_channel_id"])
        await message.answer(f"Сообщение #{post['tg_msg_channel_id']} удалено!", reply_markup=menu_back_inline_keyboard())
    elif data["type"] == "group":
        await bot.delete_message(chat_id=f"{cfg.group_id}", message_id=post["tg_msg_ans_id"])
        await methods.delete_answer(tg_msg_ans_id=post["tg_msg_ans_id"])
        await message.answer(f"Ответ #{post['tg_msg_ans_id']} удалён!", reply_markup=menu_back_inline_keyboard())
    await state.clear()




















