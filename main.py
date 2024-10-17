import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from config import TOKEN_API

from bot.handlers.user import user
from bot.handlers.admin import admin
from bot.middleware.middleware import SubscriptionMiddleware

async def main() -> None:
    bot = Bot(token=TOKEN_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(admin, user)
    dp.message.middleware(SubscriptionMiddleware())

    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("Bot started...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")