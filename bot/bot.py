from aiogram import Bot, Dispatcher
from aiogram.types import WebhookInfo

from loguru import logger

from system import first_run
from settings import get_settings, Settings

from bot.loader import bot
from bot.routers import router

cfg: Settings = get_settings()

dp = Dispatcher()

dp.include_router(router)


async def set_webhook(my_bot: Bot) -> None:
    # Check and set webhook for telegram
    async def check_webhook() -> WebhookInfo | None:
        try:
            webhook_info = await my_bot.get_webhook_info()
            return webhook_info
        except Exception as e:
            logger.error(f"Can't get webhook info - {e}")
            return

    current_webhook_info = await check_webhook()
    if cfg.debug:
        logger.debug(f"Current bot info: {current_webhook_info}")
    try:
        await bot.set_webhook(
            f"{cfg.base_webhook_url}{cfg.webhook_path}",
            secret_token=cfg.telegram_my_token,
            drop_pending_updates=current_webhook_info.pending_update_count > 0,
            max_connections=40 if cfg.debug else 100,
        )
        if cfg.debug:
            logger.debug(f"Updated bot info: {await check_webhook()}")
    except Exception as e:
        logger.error(f"Can't set webhook - {e}")


# async def set_bot_commands_menu(my_bot: Bot) -> None:
#     # Register commands for telegram bot (menu)
#     commands = [
#         BotCommand(command="/menu", description="Меню"),
#     ]
#     try:
#         await my_bot.set_my_commands(commands)
#     except Exception as e:
#         logger.error(f"Can't set commands - {e}")


async def start_telegram():
    fr = await first_run()
    if cfg.debug:
        logger.debug(f"First run: {fr}")
    if fr:
        await set_webhook(bot)
        # await set_bot_commands_menu(bot)
