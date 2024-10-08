import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest

from config import *
from middleware import SubscriptionMiddleware
from info import Ainfo

router = Router()

info = Ainfo(SERVERS)

async def delete_info_messages(
        sent_message: Message,
        message: Message) -> None:
    await asyncio.sleep(AUTO_DELETE_DELAY_TIME)
    try:
        await message.bot.delete_messages(
            chat_id=message.chat.id,
            message_ids=[sent_message.message_id, message.message_id]
        )
        # print(f"[*] Инфо: ID удаляемого сообщения: {sent_message.message_id}\n"
        #       f"[*] Инфо: Удаленное Сообщение: {sent_message.text}")
    except Exception as e:
        print(f"Ошибка удаления сообщения: {e}")

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.reply("/info")

@router.message(Command("info"))
async def cmd_info(message: Message) -> None:
    servers = await info.get_server_info(SERVERS)
    for server in servers:
        photo = server["image_url"]
        caption = f"<b>Host:</b> <code>{server['host']}</code>\n" \
                  f"<b>Server:</b> <code>{server['server_name']}</code>\n" \
                  f"<b>Map:</b> <code>{server['map_name']}</code>\n" \
                  f"<b>Players:</b> <code>{server['player_count']}/{server['max_players']}</code>\n" \
                  f"<b>Bots:</b> <code>{server['bot_count']}</code>\n\n" \
                  f"{server['players_caption']}"

        try:
            sent_message = await message.reply_photo(photo=photo, caption=caption)
        except TelegramBadRequest:
            sent_message = await message.reply(text=caption)

        # print(f"[*] Инфо: ID текущего сообщения: {sent_message.message_id}")

        await asyncio.sleep(2)

        if AUTO_DELETE_DELAY_TIME > 0:
            asyncio.create_task(delete_info_messages(message, sent_message))

async def main() -> None:
    bot = Bot(token=TOKEN_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    dp.message.middleware(SubscriptionMiddleware())

    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("Bot started...")
    except KeyboardInterrupt:
        print("Bot stopped!")