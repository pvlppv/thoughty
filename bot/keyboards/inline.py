from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from settings import get_settings

cfg = get_settings()


def menu_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Написать сообщение", callback_data="feeling")
    builder.button(text="📊 Статистика", callback_data="statistics")
    builder.adjust(1)
    return builder.as_markup()


def menu_small_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Написать сообщение", callback_data="feeling")
    return builder.as_markup()


def menu_back_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="menu")
    return builder.as_markup()


def feeling_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🟣 Любовь", callback_data="Любовь")
    builder.button(text="🟢 Радость", callback_data="Радость")
    builder.button(text="🔵 Грусть", callback_data="Грусть")
    builder.button(text="🟡 Страх", callback_data="Страх")
    builder.button(text="🔴 Гнев", callback_data="Гнев")
    builder.button(text="⬅️ Назад", callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()


def generate_feeling_inline_keyboard(feeling_category: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for feeling in [
        "Нежность", "Теплота", "Блаженство", "Доверие", "Безопасность",
        "Благодарность", "Умиротворение", "Симпатия", "Гордость",
        "Восхищение", "Уважение", "Влюблённость", "Любовь к себе",
        "Очарованность", "Забота", "Вера", "Искренность", "Доброта",
    ] if feeling_category == "Любовь" else [
        "Счастье", "Восторг", "Ликование", "Приподнятость", "Оживление",
        "Увлечение", "Интерес", "Предвкушение", "Надежда", "Любопытство",
        "Освобождение", "Принятие", "Нетерпение", "Изумление",
    ] if feeling_category == "Радость" else [
        "Горечь", "Тоска", "Скорбь", "Лень", "Жалость", "Отрешённость",
        "Отчаяние", "Беспомощность", "Душевная боль", "Безнадёжность",
        "Отчуждение", "Разочарование", "Потрясение", "Сожаление", "Скука",
        "Безысходность", "Печаль", "Загнанность",
    ] if feeling_category == "Грусть" else [
        "Ужас", "Отчаяние", "Испуг", "Оцепенение", "Подозрение", "Тревога",
        "Ошарашенность", "Беспокойство", "Боязнь", "Унижение", "Замешательство",
        "Растерянность", "Стыд", "Сомнение", "Застенчивость", "Опасение",
        "Смущенине", "Сломленность", "Подвох", "Надменность",
    ] if feeling_category == "Страх" else [
        "Бешенство", "Ярость", "Ненависть", "Истерия", "Злость", "Раздражение",
        "Презрение", "Негодование", "Обида", "Ревность", "Уязвлённость",
        "Досада", "Зависть", "Неприязнь", "Возмущение", "Отвращение",
    ]:
        builder.button(text=feeling, callback_data=f"{feeling_category}-{feeling}")
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="feeling")
    )
    return builder.as_markup()


def feeling_back_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="feeling")
    return builder.as_markup()


def post_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Изменить", callback_data="feeling")
    builder.button(text="✅ Отправить", callback_data="post")
    return builder.as_markup()


def post_channel_inline_keyboard(message_id: int = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👀 Посмотреть", callback_data="channel", url=f"https://t.me/thoughty_channel/{message_id}")
    builder.button(text="📝 Написать сообщение", callback_data="feeling")
    builder.button(text="💬 Мои сообщения", callback_data="my_posts")
    builder.adjust(1)
    return builder.as_markup()


def post_channel_small_inline_keyboard(message_id: int = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👀 Посмотреть", callback_data="channel", url=f"https://t.me/thoughty_channel/{message_id}")
    builder.adjust(1)
    return builder.as_markup()


def answer_group_inline_keyboard(message_id: int = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👀 Посмотреть", callback_data="group", url=f"https://t.me/thoughty_group/{message_id}")
    builder.button(text="💬 Мои ответы", callback_data="my_answers")
    builder.adjust(1)
    return builder.as_markup()


def answer_group_small_inline_keyboard(message_id: int = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👀 Посмотреть", callback_data="group", url=f"https://t.me/thoughty_group/{message_id}")
    builder.adjust(1)
    return builder.as_markup()


def statistics_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="❤️‍🔥 Мои чувства", callback_data="my_feelings"),
        width=1
    )
    builder.row(
        InlineKeyboardButton(text="💬 Мои сообщения", callback_data="my_posts"),
        InlineKeyboardButton(text="💬 Мои ответы", callback_data="my_answers"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="menu"),
        width=1
    )
    return builder.as_markup()


def statistics_back_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="statistics")
    return builder.as_markup()


def statistics_back_2_inline_keyboard(callback_message_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data=f"statistics_back_{callback_message_id}")
    return builder.as_markup()


def my_posts_inline_keyboard(page: int = 1, page_count: int = 1, message_id: int = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data="my_posts_prev"),
        InlineKeyboardButton(text=f"{page}/{page_count}", callback_data="1"),
        InlineKeyboardButton(text="➡️", callback_data="my_posts_next"),
        width=3
    )
    builder.row(
        InlineKeyboardButton(text="👀 Посмотреть", callback_data="channel", url=f"https://t.me/thoughty_channel/{message_id}"),
        InlineKeyboardButton(text="🗑 Удалить", callback_data="my_posts_delete"),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="statistics"),
        width=1
    )
    return builder.as_markup()


def my_posts_back_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Мои сообщения", callback_data="my_posts")
    return builder.as_markup()


def my_answers_inline_keyboard(page: int = 1, page_count: int = 1, message_id: int = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data="my_answers_prev"),
        InlineKeyboardButton(text=f"{page}/{page_count}", callback_data="1"),
        InlineKeyboardButton(text="➡️", callback_data="my_answers_next"),
        width=3
    )
    builder.row(
        InlineKeyboardButton(text="👀 Посмотреть", callback_data="group", url=f"https://t.me/thoughty_group/{message_id}"),
        InlineKeyboardButton(text="🗑 Удалить", callback_data="my_answers_delete"),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="statistics"),
        width=1
    )
    return builder.as_markup()


def my_answers_back_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Мои ответы", callback_data="my_answers")
    return builder.as_markup()


def admin_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Удалить сообщение", callback_data="admin_delete_post")
    builder.button(text="Удалить ответ", callback_data="admin_delete_answer")
    builder.button(text="⬅️ Назад", callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()


def report_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="report")
    builder.button(text="⬅️ Назад", callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()
