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
    post2_inline_keyboard,
)
from aiogram.filters import StateFilter
from aiogram.utils.markdown import hbold, hlink, hitalic

post_router = Router(name='post')
post_router.message.filter(ChatTypeFilter(chat_type=["private"]))


class State(StatesGroup):
    mood = State()
    text = State()
    

@post_router.callback_query(F.data == "mood")
async def mood_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    await callback.message.edit_text(
        text=f"{hbold("Как ты себя чувствуешь?")}\n\nВыбери из меню:",
        reply_markup=mood_inline_keyboard(),
    )
    await state.set_state(State.mood)


@post_router.callback_query(F.data.in_(["Отлично", "Хорошо", "Нормально", "Плохо"]))
async def text_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    mood = callback.data
    if mood == "Отлично":
        emoji = "🟢"
    elif mood == "Хорошо":
        emoji = "🔵"
    elif mood == "Нормально":
        emoji = "🟡"
    elif mood == "Плохо":
        emoji = "🔴"
    await state.update_data({"mood": mood, "emoji": emoji})
    await callback.message.edit_text(
        text=f"{hbold('Почему ты так себя чувствуешь?')}\n\nРаспиши:",
        reply_markup=mood_back_inline_keyboard(),
    )
    await state.set_state(State.text)

@post_router.message(State.text)
async def post_handler(message: types.Message, state: FSMContext):
    handler(__name__, type=message)
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
            f"{hbold("Настроение:")} {data["mood"]}\n"
            f"{hbold('Текст:')} {text}\n\n"
            f"{hitalic('P.S.: Неэтичные сообщения будут удалены(')}",
            reply_markup=post_inline_keyboard(),
        )

    except exceptions.TelegramBadRequest as e:
        if "message is too long" in str(e):
            await message.answer("Слишком длинное сообщение(")
            return

@post_router.callback_query(StateFilter(State), F.data == "post")
async def post_callback(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    data = await state.get_data()
    emoji = data["emoji"]
    mood = data["mood"]
    text = data["text"]
    sent_message = await bot.send_message(
        chat_id=-1002143350485,
        text=f"{emoji} Аноним чувствует себя {hbold(mood.lower())}:\n\n{text}\n\n{hlink('Ответить', 't.me/thoughty_bot/')} | {hlink('Пожаловаться', 't.me/thoughty_bot/')}", 
        parse_mode="HTML"
    )
    await callback.message.edit_text("Твоё сообщение отправлено!", reply_markup=post2_inline_keyboard())
    await methods.create_post(telegram_user_id=callback.from_user.id, telegram_message_id=sent_message.message_id, mood=mood, text=text)        
    await state.clear()


