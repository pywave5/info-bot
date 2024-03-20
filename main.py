import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest

from config import *
from info import Ainfo

bot = Bot(token=TOKEN_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

info = Ainfo(SERVERS)

@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.reply("/info")

@dp.message(Command("info"))
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

        if AUTO_DELETE_DELAY_TIME > 0:
            await asyncio.sleep(AUTO_DELETE_DELAY_TIME)
            await bot.delete_messages(
                chat_id=message.chat.id,
                message_ids=[sent_message.message_id, message.message_id]
            )

async def main() -> None:
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())