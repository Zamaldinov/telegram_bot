from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


class SlowpokeMiddleware(BaseMiddleware):
    """Мидлвари для записи истории команд юзера в БД"""
    def __init__(self, db_controller):
        self.db_controller = db_controller

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        result = await handler(event, data)
        if isinstance(event, Message) and event.text.startswith("/"):
            self.db_controller.add_history(event.from_user.id, event.text[1:])
        return result

