from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.exceptions import TelegramBadRequest

from config import CHAT_ID

class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if CHAT_ID is not None:
            try:
                chat = await event.bot.get_chat(CHAT_ID)
                status = await event.bot.get_chat_member(
                    chat_id=CHAT_ID,
                    user_id=event.from_user.id
                )
                if "left" in status.status:
                    await event.answer(
                        text=f"Вы не состоите в чате <b>{chat.title}</b>\n" 
                             f"вступите в наш чат, чтобы пользоваться ботом.\n"
                             f"Ссылка: {chat.invite_link}",
                    )
                else:
                    return await handler(event, data)
            except TelegramBadRequest:
                return await event.answer("Произошла ошибка, бот не является админстратором в чате.")
        else:
            return await handler(event, data)