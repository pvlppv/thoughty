from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Написать сообщение", callback_data="mood")
    builder.button(text="💬 Мои сообщения", callback_data="my_posts")
    builder.adjust(1)
    return builder.as_markup()


def menu_small_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Написать сообщение", callback_data="mood")
    return builder.as_markup()


def menu_small2_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Мои сообщения", callback_data="my_posts")
    return builder.as_markup()


def mood_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🟢 Отлично", callback_data="Отлично")
    builder.button(text="🔵 Хорошо", callback_data="Хорошо")
    builder.button(text="🟡 Нормально", callback_data="Нормально")
    builder.button(text="🔴 Плохо", callback_data="Плохо")
    builder.button(text="⬅️ Назад", callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()


def mood_back_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="mood")
    return builder.as_markup()


def post_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Изменить", callback_data="mood")
    builder.button(text="✅ Отправить", callback_data="post")
    return builder.as_markup()


def post2_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👀 Посмотреть", callback_data="channel", url="https://t.me/thoughty_channel")
    builder.button(text="📝 Написать сообщение", callback_data="mood")
    builder.button(text="💬 Мои сообщения", callback_data="my_posts")
    builder.adjust(1)
    return builder.as_markup()


def my_posts_inline_keyboard(page: int = 1, page_count: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data="my_posts_prev"),
        InlineKeyboardButton(text=f"{page}/{page_count}", callback_data="1"),
        InlineKeyboardButton(text="➡️", callback_data="my_posts_next"),
        width=3
    )
    builder.row(
        InlineKeyboardButton(text="🗑 Удалить", callback_data="my_posts_delete"),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="menu"),
        width=1
    )
    return builder.as_markup()


