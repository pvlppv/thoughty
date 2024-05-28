from aiogram import Router, types, F, exceptions
from bot.loader import bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.utils.logging import handler
from bot.filters.chat_type import ChatTypeFilter
from bot.utils.api_utils import methods
from bot.keyboards.inline import (
    feeling_inline_keyboard,
    feeling_back_inline_keyboard,
    post_inline_keyboard,
    post_channel_inline_keyboard,
    generate_feeling_inline_keyboard,
)
from aiogram.filters import StateFilter
from aiogram.utils.markdown import hbold, hlink, hitalic, hblockquote
from aiogram.utils.deep_linking import create_start_link
import asyncio
import re
from settings import get_settings
from bot.utils.text_utils import feeling_data, validate_text, modify_text_ending

cfg = get_settings()

post_router = Router(name='post')


class StatePost(StatesGroup):
    feeling = State()
    text = State()
    

@post_router.callback_query(F.data == "feeling")
async def feeling_category_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    await callback.answer()
    await callback.message.edit_text(
        text=f"{hbold('Что ты чувствуешь?')}",
        reply_markup=feeling_inline_keyboard(),
    )


@post_router.callback_query(F.data.in_(["Любовь", "Радость", "Грусть", "Страх", "Гнев"]))
async def feeling_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    feeling_category = callback.data
    await callback.answer()
    await callback.message.edit_text(
        text=f"{hbold('Что ты чувствуешь?')}",
        reply_markup=generate_feeling_inline_keyboard(feeling_category),
    )
    await state.set_state(StatePost.feeling)


@post_router.callback_query(F.data.contains("-"))
async def feeling_text_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    feeling_category, feeling = callback.data.split("-")
    emoji = feeling_data[feeling_category]
    await state.update_data({"feeling_category": feeling_category, "feeling": feeling, "emoji": emoji})
    await callback.answer()
    await callback.message.edit_text(
        text=
        f"{hbold('Почему ты это чувствуешь?')}\n\n"
        f"{hitalic('Ты можешь рассказать о том, что вызвало ')}"
        f"{hbold(modify_text_ending(feeling).lower())}: "
        f"{hitalic('недавние события, поступки или слова окружающих, твоё духовное или физическое состояние')}",
        reply_markup=feeling_back_inline_keyboard(),
    )
    await state.set_state(StatePost.text)


@post_router.message(ChatTypeFilter(chat_type=["private"]), StatePost.text)
async def post_handler(message: types.Message, state: FSMContext):
    handler(__name__, type=message)
    try:
        text = message.text
        if not validate_text(text):
            await message.answer("Твоё сообщение не прошло проверки, проверь, чтобы оно не содержало стикеры/фото/видео/голосовые, запрещённые символы, ссылки")
            return
        if len(text) < 20:
            await message.answer("Слишком короткое сообщение(")
            return
        data = await state.get_data()
        await state.update_data({"text": text})
        await message.answer(
            text=
            f"{hbold('Твоё сообщение:')}\n\n"
            f"{data['emoji']} {data['feeling']}\n"
            f"{text}\n\n"
            f"{hlink('Правила публикации', 'https://telegra.ph/Pravila-publikacii-soobshchenij-Soti-05-04')}",
            reply_markup=post_inline_keyboard(),
            disable_web_page_preview=True,
        )
    except exceptions.TelegramBadRequest as e:
        if "message is too long" in str(e):
            await message.answer("Слишком длинное сообщение(")
            return


@post_router.callback_query(StateFilter(StatePost), F.data == "post")
async def post_callback(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    data = await state.get_data()
    emoji = data["emoji"]
    feeling_category = data["feeling_category"]
    feeling = data["feeling"]
    text = data["text"]
    sent_message = await bot.send_message(
        chat_id=cfg.channel_id,
        text=f"{emoji} Аноним чувствует {hbold(modify_text_ending(feeling).lower())}:\n\n{text}"
    )
    await bot.edit_message_text(
        chat_id=cfg.channel_id,
        message_id=sent_message.message_id,
        text=f"{emoji} Аноним чувствует {hbold(modify_text_ending(feeling).lower())}:\n\n{text}\n\n#{sent_message.message_id}"
    )
    await callback.answer()
    await callback.message.edit_text("Твоё сообщение отправлено!", reply_markup=post_channel_inline_keyboard(sent_message.message_id))
    await methods.create_post(
        tg_user_id=callback.from_user.id,
        tg_msg_channel_id=sent_message.message_id,
        feeling_category=feeling_category,
        feeling=feeling,
        text=text
    )
    await state.clear()


@post_router.message(ChatTypeFilter(chat_type=["supergroup"]))
async def group_message_handler(message: types.Message):
    handler(__name__, type=message)
    if not message.text:
        return
    text = message.text
    matches = re.findall(r'#(\d+)', text)  # Search for all ID patterns
    if not matches:
        return
    message_id = matches[-1]  # Extract the last ID
    await methods.update_post(tg_msg_channel_id=message_id, tg_msg_group_id=message.message_id)
    answer = await create_start_link(bot, f"answer-{message.message_id}")
    report = await create_start_link(bot, f"report-{message.message_id}")
    post = await methods.get_post_by_tg_msg_channel_id(tg_msg_channel_id=message_id)
    feeling_category = post['feeling_category']
    feeling = post['feeling']
    text = post['text']
    emoji = feeling_data[feeling_category]
    await bot.edit_message_text(
        chat_id=cfg.channel_id,
        message_id=message_id,
        text=f"{emoji} Аноним чувствует {hbold(modify_text_ending(feeling).lower())}:\n\n{text}\n\n"
        f"{hlink('Ответить', f'{answer}')} | "
        f"{hlink('Пожаловаться', f'{report}')}",
        disable_web_page_preview=True,
    )
