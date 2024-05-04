from aiogram import Router, types, F, exceptions
from bot.loader import bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.utils.logging import handler
from bot.filters.chat_type import ChatTypeFilter
from bot.utils.api_utils import methods

from bot.keyboards.inline import (
    menu_small_inline_keyboard,
    menu_back_inline_keyboard,
    my_posts_inline_keyboard,
    my_posts_back_inline_keyboard,
    my_answers_inline_keyboard,
    my_answers_back_inline_keyboard
)
from aiogram.utils.markdown import hbold
from datetime import datetime
from aiogram.filters import StateFilter, Command
from aiogram.utils.markdown import hlink

settings_router = Router(name='settings')
settings_router.message.filter(ChatTypeFilter(chat_type=["private"]))


class StateMyPosts(StatesGroup):
    page = State()
    posts = State()


class StateMyAnswers(StatesGroup):
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
            f"{hbold('Настроение:')} {post['mood']}\n"
            f"{hbold('Текст:')} {post['text']}\n"
            f"{hbold('Дата:')} {datetime.fromisoformat(post['created_at']).strftime('%H:%M, %d.%m.%Y')}\n\n"
        ),
        reply_markup=my_posts_inline_keyboard(page, len(posts), post["tg_msg_channel_id"]),
    )


@settings_router.callback_query(F.data == "my_posts")
async def my_posts_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    posts = await methods.get_posts_by_tg_user_id(tg_user_id=callback.from_user.id)
    if not posts:
        await callback.message.edit_text(
            text="У тебя пока нет сообщений, напиши первое :)",
            reply_markup=menu_small_inline_keyboard(),
        )
        return
    await state.set_state(StateMyPosts.page)
    await state.update_data({"posts": posts})
    await edit_posts_message_handler(callback, state, 1)


@settings_router.callback_query(StateFilter(StateMyPosts), F.data == "my_posts_prev")
async def my_posts_prev_page_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    data = await state.get_data()
    await edit_posts_message_handler(callback, state, data["page"] - 1)


@settings_router.callback_query(StateFilter(StateMyPosts), F.data == "my_posts_next")
async def my_posts_next_page_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    data = await state.get_data()
    await edit_posts_message_handler(callback, state, data["page"] + 1)


@settings_router.callback_query(StateFilter(StateMyPosts), F.data == "my_posts_delete")
async def delete_post_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    try:
        data = await state.get_data()
        tg_msg_channel_id = data["posts"][data["page"] - 1]["tg_msg_channel_id"]
        await bot.delete_message(chat_id=-1002143350485, message_id=tg_msg_channel_id)
        await methods.delete_post(tg_msg_channel_id=tg_msg_channel_id)
        await callback.message.edit_text(text="Сообщение удалено!", reply_markup=my_posts_back_inline_keyboard())
        await state.clear()
    except exceptions.TelegramBadRequest:
        await callback.message.edit_text("Внутренняя ошибка: соообщение уже удалено в канале, обратитесь к @pvlppv.")
        return


async def edit_answers_message_handler(callback: types.CallbackQuery, state: FSMContext, page: int):
    handler(__name__, type=callback)
    data = await state.get_data()
    answers = data["answers"]
    if page < 1 or page > len(answers):
        await callback.answer("Неверный номер страницы", show_alert=True)
        return
    answer = answers[page - 1]
    await state.update_data({"page": page, "pages": len(answers)})
    await callback.message.edit_text(
        text=(
            f"{hbold('Исходное сообщение:')} {answer['msg_group_text']}\n"
            f"{hbold('Твой ответ:')} {answer['msg_ans_text']}\n"
            f"{hbold('Дата:')} {datetime.fromisoformat(answer['created_at']).strftime('%H:%M, %d.%m.%Y')}\n\n"
        ),
        reply_markup=my_answers_inline_keyboard(page, len(answers), answer["tg_msg_ans_id"]),
    )


@settings_router.callback_query(F.data == "my_answers")
async def my_answers_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    answers = await methods.get_answers_by_tg_user_id(tg_user_id=callback.from_user.id)
    if not answers:
        await callback.message.edit_text(
            text=f"У тебя пока нет ответов, переходи в {hlink('канал', 'https://t.me/thoughty_channel')} и отвечай на сообщения :)",
            reply_markup=menu_back_inline_keyboard(),
        )
        return
    await state.set_state(StateMyAnswers.page)
    await state.update_data({"answers": answers})
    await edit_answers_message_handler(callback, state, 1)


@settings_router.callback_query(StateFilter(StateMyAnswers), F.data == "my_answers_prev")
async def my_answers_prev_page_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await edit_answers_message_handler(callback, state, data["page"] - 1)


@settings_router.callback_query(StateFilter(StateMyAnswers), F.data == "my_answers_next")
async def my_answers_next_page_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await edit_answers_message_handler(callback, state, data["page"] + 1)


@settings_router.callback_query(StateFilter(StateMyAnswers), F.data == "my_answers_delete")
async def delete_answer_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    try:
        data = await state.get_data()
        tg_msg_ans_id = data["answers"][data["page"] - 1]["tg_msg_ans_id"]
        await bot.delete_message(chat_id=-1002142761767, message_id=tg_msg_ans_id)
        await methods.delete_answer(tg_msg_ans_id=tg_msg_ans_id)
        await callback.message.edit_text(text="Ответ удалён!", reply_markup=my_answers_back_inline_keyboard())
        await state.clear()
    except exceptions.TelegramBadRequest:
        await callback.message.edit_text("Внутренняя ошибка: ответ уже удалён в канале, обратитесь к @pvlppv.")
        return