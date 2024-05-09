from aiogram import Router, types, F, exceptions
from bot.loader import bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.utils.logging import handler
from bot.filters.chat_type import ChatTypeFilter
from bot.utils.api_utils import methods
from bot.keyboards.inline import (
    menu_small_inline_keyboard,
    my_posts_inline_keyboard,
    my_posts_back_inline_keyboard,
    my_answers_inline_keyboard,
    my_answers_back_inline_keyboard,
    statistics_inline_keyboard,
    statistics_back_inline_keyboard,
    statistics_back_2_inline_keyboard,
    post_channel_small_inline_keyboard,
)
from aiogram.utils.markdown import hbold, hblockquote
from datetime import datetime
from aiogram.filters import StateFilter
from aiogram.utils.markdown import hlink
from settings import get_settings
from bot.utils.text_utils import feeling_data
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

cfg = get_settings()

settings_router = Router(name='settings')
settings_router.message.filter(ChatTypeFilter(chat_type=["private"]))


class StateMyPosts(StatesGroup):
    page = State()
    posts = State()


class StateMyAnswers(StatesGroup):
    page = State()
    posts = State()


@settings_router.callback_query(F.data == "statistics")
async def statistics_handler(callback: types.CallbackQuery):
    handler(__name__, type=callback)
    await callback.message.edit_text(
        text=f"📊 {hbold('Статистика:')}",
        reply_markup=statistics_inline_keyboard(),
    )


@settings_router.callback_query(F.data.contains("statistics_back_"))
async def statistics_back_handler(callback: types.CallbackQuery):
    handler(__name__, type=callback)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.data.split("_")[-1])
    await callback.message.delete()
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"📊 {hbold('Статистика:')}",
        reply_markup=statistics_inline_keyboard(),
    )


@settings_router.callback_query(F.data == "my_feelings")
async def my_statistics_handler(callback: types.CallbackQuery):
    handler(__name__, type=callback)

    # Line chart
    data_line = await methods.get_last_posts(tg_user_id=callback.from_user.id)
    if not data_line:
        await callback.message.edit_text(
            text="У тебя пока нет сообщений, напиши первое :)",
            reply_markup=menu_small_inline_keyboard(),
        )
        return

    await bot.send_chat_action(chat_id=callback.from_user.id, action="upload_photo")

    wait_message = await callback.message.edit_text("Рисую графики...")

    feelings_mapping = {"Гнев": 1, "Страх": 2, "Грусть": 3, "Радость": 4, "Любовь": 5}
    df_line = pd.DataFrame(data_line)
    df_line["feeling_value"] = df_line["feeling_category"].map(feelings_mapping)

    df_line["created_at"] = pd.to_datetime(df_line["created_at"])
    df_line.sort_values(by="created_at", inplace=True)

    end_date = pd.Timestamp.today(tz="Europe/Moscow").normalize()
    start_date = end_date - pd.Timedelta(days=6)
    padding = pd.Timedelta(days=1)
    xasis_range = [start_date, end_date + padding]

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=df_line["created_at"], y=df_line["feeling_value"], mode="lines+markers", line={"color": "white", "width": 2, "smoothing": 1.3}))
    fig_line.update_layout(
        title="Мои чувства за последнюю неделю",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font={"color": "white", "family": "Montserrat"},
        xaxis={
            "tickformat": "%d.%m",
            "range": xasis_range,
            "zeroline": False,
            "gridcolor": "rgba(255, 255, 255, 0.3)",
            "gridwidth": 0.5,
        },
        yaxis={
            "tickvals": list(feelings_mapping.values()),
            "ticktext": list(feelings_mapping.keys()),
            "range": [min(feelings_mapping.values()) - 1, max(feelings_mapping.values()) + 1],
            "zeroline": False,
            "gridcolor": "rgba(255, 255, 255, 0.3)",
            "gridwidth": 0.5,
        },
    )

    # Pie chart
    data_pie = await methods.get_posts_by_tg_user_id(tg_user_id=callback.from_user.id)
    feelings_mapping2 = {"Любовь": "purple", "Радость": "green", "Грусть": "blue", "Страх": "yellow", "Гнев": "red"}
    df_pie = pd.DataFrame(data_pie)
    df_pie["color"] = df_pie["feeling_category"].map(feelings_mapping2)
    feeling_color_count = df_pie.groupby(["feeling_category", "color"]).size().reset_index(name="count")

    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(labels=feeling_color_count["feeling_category"], values=feeling_color_count["count"], hole=0.4, marker={"colors": feeling_color_count["color"]}))
    fig_pie.update_layout(
        title="Моё распределение чувств",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font={"color": "white", "family": "Montserrat"},
        legend={"font": {"color": "white"}, "bgcolor": "black", "x": -0.1, "y": 1, "xanchor": "left", "yanchor": "top"},
    )

    layot_name = {
        "text": "Соти",
        "xref": "paper",
        "yref": "paper",
        "x": 1,
        "y": 1.14,
        "xanchor": "right",
        "yanchor": "bottom",
        "showarrow": False,
        "font": {"size": 20, "color": "white", "weight": "bold"},
    }
    layot_username = {
        "text": "@thoughty_channel",
        "xref": "paper",
        "yref": "paper",
        "x": 1.028,
        "y": 1.115,
        "xanchor": "right",
        "yanchor": "bottom",
        "showarrow": False,
        "font": {"size": 8, "color": "white"},
    }
    fig_line.add_annotation(**layot_name)
    fig_line.add_annotation(**layot_username)

    fig_pie.add_annotation(**layot_name)
    fig_pie.add_annotation(**layot_username)

    wait_message = await callback.message.edit_text("Отправляю графики...")

    img_bytes_line = fig_line.to_image(format="png", scale=1.5)
    img_bytes_pie = fig_pie.to_image(format="png", scale=1.5)
    await wait_message.delete()
    line = await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=types.BufferedInputFile(img_bytes_line, "line_plot.png"),
    )
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=types.BufferedInputFile(img_bytes_pie, "pie_plot.png"),
        reply_markup=statistics_back_2_inline_keyboard(line.message_id),
    )


async def edit_posts_message_handler(callback: types.CallbackQuery, state: FSMContext, page: int):
    handler(__name__, type=callback)
    data = await state.get_data()
    posts = data["posts"]
    if page < 1 or page > len(posts):
        await callback.answer("Неверный номер страницы", show_alert=True)
        return
    post = posts[page - 1]
    await state.update_data({"page": page, "pages": len(posts)})
    feeling_category = post["feeling_category"]
    feeling = post["feeling"]
    emoji = feeling_data[feeling_category]
    answer_count = post["answer_count"]
    await callback.message.edit_text(
        text=(
            f"{emoji} {feeling}\n\n"
            f"{post['text']}\n\n"
            f"💬: {answer_count}\n"
            f"🗓 {datetime.fromisoformat(post['created_at']).strftime('%H:%M, %d.%m.%Y')}"
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
        await bot.delete_message(chat_id=cfg.channel_id, message_id=tg_msg_channel_id)
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
            f"{hbold('Исходное сообщение:')}\n"
            f"{hblockquote(answer['msg_group_text'])}\n\n"
            f"{hbold('Твой ответ:')}\n"
            f"{hblockquote(answer['msg_ans_text'])}\n\n"
            f"🗓 {datetime.fromisoformat(answer['created_at']).strftime('%H:%M, %d.%m.%Y')}"
        ),
        reply_markup=my_answers_inline_keyboard(page, len(answers), answer["tg_msg_ans_id"]),
    )


@settings_router.callback_query(F.data == "my_answers")
async def my_answers_handler(callback: types.CallbackQuery, state: FSMContext):
    handler(__name__, type=callback)
    answers = await methods.get_answers_by_tg_user_id(tg_user_id=callback.from_user.id)
    if not answers:
        await callback.message.edit_text(
            text=f"У тебя пока нет ответов, переходи в {hlink('канал', f'https://t.me/thoughty_channel')} и отвечай на сообщения :)",
            reply_markup=statistics_back_inline_keyboard(),
            disable_web_page_preview=True,
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
        tg_msg_group_id = data["answers"][data["page"] - 1]["tg_msg_group_id"]
        await bot.delete_message(chat_id=cfg.group_id, message_id=tg_msg_ans_id)
        await methods.delete_answer(tg_msg_ans_id=tg_msg_ans_id, tg_msg_group_id=tg_msg_group_id)
        await callback.message.edit_text(text="Ответ удалён!", reply_markup=my_answers_back_inline_keyboard())
        await state.clear()
    except exceptions.TelegramBadRequest:
        await callback.message.edit_text("Внутренняя ошибка: ответ уже удалён в канале, обратитесь к @pvlppv.")
        return
    

@settings_router.message_reaction_count()
async def message_reaction_count_handler(message_reaction_count: types.MessageReactionCountUpdated):
    tg_msg_channel_id = message_reaction_count.message_id
    reactions_count = len(message_reaction_count.reactions)
    post = await methods.get_post_by_tg_msg_channel_id(tg_msg_channel_id=tg_msg_channel_id)
    if post["like_count"] < reactions_count:
        await bot.send_message(
            chat_id=post["tg_user_id"],
            text=f"Тебе поставили лайк!",
            reply_markup=post_channel_small_inline_keyboard(message_id=tg_msg_channel_id),
        )
    await methods.update_post_like_count(tg_msg_channel_id=tg_msg_channel_id, like_count=reactions_count)
