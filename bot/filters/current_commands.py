from aiogram.filters import BaseFilter
from aiogram.types.message import Message

class CurrentCommands(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text not in ["/start", "/info", "/add", "/help", "remove"]