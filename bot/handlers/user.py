import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.exceptions import TelegramBadRequest

from bot.handlers.info import Ainfo
from bot.handlers.admin import json_file_handler
from config import *

user = Router()
server_info = Ainfo(servers=SERVERS)

async def delete_info_messages(
        sent_message: Message,
        message: Message) -> None:
    await asyncio.sleep(AUTO_DELETE_DELAY_TIME)
    try:
        await message.bot.delete_messages(
            chat_id=message.chat.id,
            message_ids=[sent_message.message_id, message.message_id]
        )
    except Exception as e:
        print(f"Ошибка удаления сообщения: {e}")

@user.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.reply("/info")

@user.message(Command("info"))
async def cmd_info(message: Message) -> None:
    servers = await server_info.get_server_info(SERVERS)
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

        await asyncio.sleep(2)

        if AUTO_DELETE_DELAY_TIME > 0:
            asyncio.create_task(delete_info_messages(message, sent_message))

@user.message(Command("help"))
async def get_commands(message: Message) -> None:
    data = await json_file_handler.load_commands()

    if not data:
        await message.answer("Нет доступных команд.")
        return

    commands_list = "\n\n".join([f"<b>Команда:</b> {cmd_data['command']}\n"
                                 f"<b>Описание:</b> {cmd_data['description']}"
                                 for cmd_data in data.values()])

    await message.answer(f"Доступные команды:\n\n{commands_list}")

@user.message(F.text.startswith("/"))
async def answer_commands(message: Message) -> None:
    data = await json_file_handler.load_commands()

    for cmd_data in data.values():
        if cmd_data['command'] == message.text:
            await message.answer(f"{cmd_data['description']}")