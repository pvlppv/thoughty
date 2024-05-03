from aiogram import Bot
from aiogram.enums import ParseMode
from settings import get_settings, Settings

cfg: Settings = get_settings()

bot = Bot(token=cfg.bot_token, parse_mode=ParseMode.HTML)

__all__ = ['bot']