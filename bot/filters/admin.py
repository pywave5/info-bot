from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import ADMINS_IDS

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS_IDS