from aiogram import types, F, Router, exceptions
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.markdown import hlink
from aiogram.types import Message
from bot.utils.logging import handler
from bot.filters.chat_type import ChatTypeFilter
from bot.utils.api_utils import methods
from bot.keyboards.inline import (
    menu_inline_keyboard,
    answer_group_inline_keyboard,
    answer_group_small_inline_keyboard,
    menu_back_inline_keyboard,
    report_inline_keyboard,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold, hitalic, hblockquote
from bot.loader import bot
from aiogram.fsm.state import State, StatesGroup
from settings import get_settings
from aiogram.filters import StateFilter
from bot.utils.text_utils import validate_text

cfg = get_settings()

menu_router = Router(name="menu")
menu_router.message.filter(ChatTypeFilter(chat_type=["private"]))


class StateAnswer(StatesGroup):
    text = State()


class StateReport(StatesGroup):
    answer = State()


@menu_router.message(CommandStart())
@menu_router.message(CommandStart(deep_link=True))
async def menu_handler(message: Message, command: CommandObject, state: FSMContext):
    handler(__name__, type=message)
    await state.clear()
    await methods.create_user(tg_user_id=message.from_user.id)
    if not command.args or command.args == "start":
        await message.answer(
            text=
            f"Привет! Соти - это {hlink('социальный дневник чувств', f'https://t.me/thoughty_channel')} Вышкинцев\n\n"
            "В этом боте ты взаимодействуешь с ним: создаёшь свои сообщения, отвечаешь на чужие, смотришь свою статистику и так далее\n\n"
            "Здесь всё анонимно, в базе данных мы храним только твой телеграм айди, поэтому и регистрации никакой нет, собственно всё :)\n\n"
            "Кликай в меню ниже:",
            reply_markup=menu_inline_keyboard(),
            disable_web_page_preview=True,
        )
    else:
        action, message_id = command.args.split("-")
        if action == "answer":
            post = await methods.get_post_by_tg_msg_group_id(tg_msg_group_id=message_id)
            if post is None:
                await message.answer("Сообщение не найдено")
                return
            await message.answer(
                text=
                f"Напиши свой ответ этому сообщению:\n\n"
                f"{hblockquote(post['text'])}",
                reply_markup=menu_back_inline_keyboard(),
            )
            await state.set_state(StateAnswer.text)
            await state.update_data(
                {
                    "tg_msg_channel_id": post["tg_msg_channel_id"],
                    "tg_msg_group_id": message_id,
                    "msg_group_text": post["text"],
                    "tg_user_id": post["tg_user_id"],
                }
            )
        elif action == "report":
            post = await methods.get_post_by_tg_msg_group_id(tg_msg_group_id=message_id)
            if post is None:
                await message.answer("Сообщение не найдено")
                return
            if message.from_user.id in post["reported_by"]:
                await message.answer(
                    "Ты уже пожаловался на это сообщение!",
                    reply_markup=menu_back_inline_keyboard(),
                )
                return
            await message.answer(text=f"Отправить жалобу на это сообщение?\n\n{hblockquote(post['text'])}", reply_markup=report_inline_keyboard())
            await state.set_state(StateReport.answer)
            await state.update_data({"tg_msg_group_id": post["tg_msg_group_id"], "tg_user_id": message.from_user.id})


@menu_router.message(StateAnswer.text)
async def answer_handler(message: Message, state: FSMContext):
    handler(__name__, type=message)
    try:
        text = message.text
        if not validate_text(text):
            await message.answer("Твоё сообщение не прошло проверки, проверь, чтобы оно не содержало стикеры/фото/видео/голосовые, запрещённые символы, ссылки")
            return
        data = await state.get_data()
        sent_message = await bot.send_message(
            chat_id=cfg.group_id,
            text = f"{hbold('Ответ от автора:' if message.from_user.id == data['tg_user_id'] else 'Ответ от анонима:')}\n{message.text}",
            reply_to_message_id=data["tg_msg_group_id"],
        )
        await message.answer(f"Твой ответ отправлен!", reply_markup=answer_group_inline_keyboard(sent_message.message_id))
        await methods.create_answer(
            tg_user_id=message.from_user.id,
            tg_msg_group_id=data["tg_msg_group_id"],
            tg_msg_ans_id=sent_message.message_id,
            msg_group_text=data["msg_group_text"],
            msg_ans_text=message.text
        )
        await state.clear()
        if data["tg_user_id"] != message.from_user.id:
            try:
                await bot.send_message(chat_id=data["tg_user_id"], text=f"На твоё сообщение ответили!", reply_markup=answer_group_small_inline_keyboard(sent_message.message_id))
            except exceptions.TelegramForbiddenError:
                pass
    except exceptions.TelegramBadRequest as e:
        if "message is too long" in str(e):
            await message.answer("Слишком длинное сообщение(")
            return


@menu_router.callback_query(StateFilter(StateReport), F.data == "report")
async def report_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    data = await state.get_data()
    post = await methods.update_post_report(tg_msg_group_id=data["tg_msg_group_id"], tg_user_id=data["tg_user_id"])
    await bot.send_message(
        chat_id=384993580,
        text=
        f"{hbold('Новая жалоба!')}\n\n"
        f"{hblockquote(post['text'])}\n\n"
        f"{hlink('Перейти', f'https://t.me/thoughty_channel/' + str(post['tg_msg_channel_id']))}",
        disable_web_page_preview=True,
    )
    if post["report_count"] >= 10:
        await bot.delete_message(chat_id=cfg.channel_id, message_id=post["tg_msg_channel_id"])
        await methods.delete_post(tg_msg_channel_id=post["tg_msg_channel_id"])
        await callback.answer()
        await callback.message.edit_text(
            "Ты пожаловался на это сообщение:\n\n"
            f"{hblockquote(post['text'])}\n\n"
            f"Жалоб у сообщения: {hbold(post['report_count'])}\n"
            f"{hitalic('Поскольку у сообщения набралось 10 жалоб, оно удаляется')}",
            reply_markup=menu_back_inline_keyboard(),
        )
    else:
        await callback.answer()
        await callback.message.edit_text(
            "Ты пожаловался на это сообщение:\n\n"
            f"{hblockquote(post['text'])}\n\n"
            f"Жалоб у сообщения: {hbold(post['report_count'])}\n"
            f"{hitalic('Как только у сообщения наберётся 10 жалоб, оно будет удалено')}",
            reply_markup=menu_back_inline_keyboard(),
        )


@menu_router.callback_query(F.data == "menu")
async def menu_handler_callback(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        text=
        f"Привет! Соти - это {hlink('социальный дневник чувств', f'https://t.me/thoughty_channel')} Вышкинцев\n\n"
        "В этом боте ты взаимодействуешь с ним: создаёшь свои сообщения, отвечаешь на чужие, смотришь свою статистику и так далее\n\n"
        "Здесь всё анонимно, в базе данных мы храним только твой телеграм айди, поэтому и регистрации никакой нет, собственно всё :)\n\n"
        "Кликай в меню ниже:",
        reply_markup=menu_inline_keyboard(),
        disable_web_page_preview=True,
    )
