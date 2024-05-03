from aiogram import Router, types, F
from bot.loader import bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.utils.logging import handler
from bot.filters.chat_type import ChatTypeFilter
from bot.utils.api_utils import methods
from bot.keyboards.inline import my_posts_inline_keyboard, menu_small_inline_keyboard, menu_small2_inline_keyboard
from aiogram.utils.markdown import hbold
from datetime import datetime
from aiogram.filters import StateFilter

settings_router = Router(name='settings')
settings_router.message.filter(ChatTypeFilter(chat_type=["private"]))


class State(StatesGroup):
    page = State()
    posts = State()


async def edit_posts_message_handler(callback: types.CallbackQuery, state: FSMContext, page: int):
    handler(__name__, type=callback)
    data = await state.get_data()
    posts = data["posts"]
    if page < 1 or page > len(posts):
        await callback.answer("Неверный номер страницы", show_alert=True)
        return
    post = posts[page - 1]
    await state.update_data({"page": page, "pages": len(posts)})
    await callback.message.edit_text(
        text=(
            f"{hbold('Твои сообщения:')}\n\n"
            f"{hbold('Настроение:')} {post['mood']}\n"
            f"{hbold('Текст:')} {post['text']}\n"
            f"{hbold('Дата:')} {datetime.fromisoformat(post['created_at']).strftime('%H:%M, %d.%m.%Y')}\n\n"
        ),
        reply_markup=my_posts_inline_keyboard(page, len(posts)),
    )


@settings_router.callback_query(F.data == "my_posts")
async def my_posts_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(State.page)
    posts = await methods.get_posts_by_tg_user_id(telegram_user_id=callback.from_user.id)
    if not posts:
        await callback.message.edit_text(
            text="У тебя пока нет сообщений, напиши первое :)",
            reply_markup=menu_small_inline_keyboard(),
        )
        return
    await state.update_data({"posts": posts})
    await edit_posts_message_handler(callback, state, 1)


@settings_router.callback_query(StateFilter(State), F.data == "my_posts_prev")
async def prev_page_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await edit_posts_message_handler(callback, state, data["page"] - 1)


@settings_router.callback_query(StateFilter(State), F.data == "my_posts_next")
async def next_page_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await edit_posts_message_handler(callback, state, data["page"] + 1)


@settings_router.callback_query(StateFilter(State), F.data == "my_posts_delete")
async def delete_post_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    data = await state.get_data()
    telegram_message_id = data["posts"][data["page"] - 1]["telegram_message_id"]
    await bot.delete_message(chat_id=-1002143350485, message_id=telegram_message_id)
    await methods.delete_post(telegram_message_id=telegram_message_id)
    await callback.message.edit_text(text="Сообщение удалено!", reply_markup=menu_small2_inline_keyboard())
