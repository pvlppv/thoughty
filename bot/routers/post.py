from aiogram import Router, types, F, exceptions
from bot.loader import bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.utils.logging import handler
from bot.filters.chat_type import ChatTypeFilter
from bot.utils.api_utils import methods
from bot.keyboards.inline import (
    mood_inline_keyboard,
    mood_back_inline_keyboard,
    post_inline_keyboard,
    answer_channel_inline_keyboard,
)
from aiogram.filters import StateFilter
from aiogram.utils.markdown import hbold, hlink, hitalic
from aiogram.utils.deep_linking import create_start_link
import asyncio
import re
from settings import get_settings

cfg = get_settings()

post_router = Router(name='post')


class StatePost(StatesGroup):
    mood = State()
    text = State()
    

@post_router.callback_query(F.data == "mood")
async def mood_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    await callback.message.edit_text(
        text=f"{hbold('Как ты себя чувствуешь?')}",
        reply_markup=mood_inline_keyboard(),
    )
    await state.set_state(StatePost.mood)


@post_router.callback_query(F.data.in_(["Прекрасно", "Отлично", "Хорошо", "Нормально", "Не очень", "Плохо"]))
async def text_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    mood = callback.data
    if mood == "Прекрасно":
        emoji = "🟣"
    elif mood == "Отлично":
        emoji = "🟢"
    elif mood == "Хорошо":
        emoji = "🔵"
    elif mood == "Нормально":
        emoji = "🟡"
    elif mood == "Не очень":
        emoji = "🟠"
    elif mood == "Плохо":
        emoji = "🔴"
    await state.update_data({"mood": mood, "emoji": emoji})
    await callback.message.edit_text(
        text=
        f"{hbold('Почему ты так себя чувствуешь?')}\n\n"
        f"{hitalic('Ты можешь рассказать о том, что повлияло на твои чувства, о недавних событиях или же просто о сегодняшнем дне:')}",
        reply_markup=mood_back_inline_keyboard(),
    )
    await state.set_state(StatePost.text)

@post_router.message(ChatTypeFilter(chat_type=["private"]), StatePost.text)
async def post_handler(message: types.Message, state: FSMContext):
    handler(__name__, type=message)
    if message.text is None:
        return
    try:
        text = message.text
        data = await state.get_data()
        await state.update_data({"text": text})
        if len(text) < 20:
            await message.answer("Слишком короткое сообщение(")
            return
        await message.answer(
            text=
            f"{hbold('Твоё сообщение:')}\n\n"
            f"{hbold('Настроение:')} {data['mood']}\n"
            f"{hbold('Текст:')} {text}\n\n"
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
    mood = data["mood"]
    text = data["text"]
    sent_message = await bot.send_message(
        chat_id=cfg.channel_id,
        text=f"{emoji} Аноним чувствует себя {hbold(mood.lower())}:\n\n{text}"
    )
    await bot.edit_message_text(
        chat_id=cfg.channel_id,
        message_id=sent_message.message_id,
        text=f"{emoji} Аноним чувствует себя {hbold(mood.lower())}:\n\n{text}\n\n#{sent_message.message_id}"
    )
    await callback.message.edit_text("Твоё сообщение отправлено!", reply_markup=answer_channel_inline_keyboard(sent_message.message_id))
    await methods.create_post(tg_user_id=callback.from_user.id, tg_msg_channel_id=sent_message.message_id, mood=mood, text=text)
    await state.clear()


@post_router.message(ChatTypeFilter(chat_type=["supergroup"]))
async def group_message_handler(message: types.Message):
    handler(__name__, type=message)
    text = message.text
    matches = re.findall(r'#(\d+)', text)  # Search for all ID patterns
    message_id = matches[-1]  # Extract the last ID
    await methods.update_post(tg_msg_channel_id=message_id, tg_msg_group_id=message.message_id)
    answer = await create_start_link(bot, f"answer-{message.message_id}")
    report = await create_start_link(bot, f"report-{message.message_id}")
    post = await methods.get_post_by_tg_msg_channel_id(tg_msg_channel_id=message_id)
    mood = post['mood']
    text = post['text']
    if mood == "Прекрасно":
        emoji = "🟣"
    elif mood == "Отлично":
        emoji = "🟢"
    elif mood == "Хорошо":
        emoji = "🔵"
    elif mood == "Нормально":
        emoji = "🟡"
    elif mood == "Не очень":
        emoji = "🟠"
    elif mood == "Плохо":
        emoji = "🔴"
    await bot.edit_message_text(
        chat_id=cfg.channel_id,
        message_id=message_id,
        text=f"{emoji} Аноним чувствует себя {hbold(mood.lower())}:\n\n{text}\n\n"
        f"{hlink('Ответить', f'{answer}')} | "
        f"{hlink('Пожаловаться', f'{report}')}",
        disable_web_page_preview=True,
    )
