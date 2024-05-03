import typing
from loguru import logger
from aiogram import types


def set_logger() -> None:
    return logger.add(
        sink="./logs.log",
        enqueue=False,
        backtrace=False,
        catch=False,
    )


def handler(
        func,
        type: typing.Union[types.Message, types.CallbackQuery],
) -> None:
    """log info from user message/callback

    args:
        func: function name (__name__)
        **type: Message | CallbackQuery: user message/callback

    returns:
        something like this
        `datetime | INFO     | utils.log_info:message:6 - function_name from fullname (@username) id: user_id`
    """
    return logger.info(
        "{mes}, id: {id}",
        mes=func,
        id=type.from_user.id,
    )