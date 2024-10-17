from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot.filters.admin import IsAdmin
from bot.filters.current_commands import CurrentCommands
from bot.state.commands import CommandState
from bot.helpers.helper import JsonFileHandler

admin = Router()
json_file_handler = JsonFileHandler("commands.json")

@admin.message(Command("add"), IsAdmin())
async def cmd_commands(message: Message, state: FSMContext) -> None:
    await message.answer("Введите команду, которую хотите добавить.\nПример: /vip")
    await state.set_state(CommandState.command)

@admin.message(F.text.regexp(r'\/[^\/\s]+'), CommandState.command, IsAdmin(), CurrentCommands())
async def cmd_command_input(message: Message, state: FSMContext) -> None:
    data = await json_file_handler.load_commands()

    for cmd_data in data.values():
        if cmd_data['command'] == message.text:
            await message.answer(f"Команда {message.text} уже существует!")
            await state.clear()
            return

    await state.update_data(command=message.text)
    await message.answer(f"Введите описание для команды {message.text}:\nПример:\n"
                         f"<blockquote>Какое-то <b>описание</b></blockquote>",
                         parse_mode=ParseMode.HTML)
    await state.set_state(CommandState.description)

@admin.message(CommandState.description)
async def cmd_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    data = await state.get_data()

    await message.answer(f"Команда успешно добавлена!\n"
                         f"Команда - {data['command']}\n"
                         f"Описание команды - {data['description']}",
                         parse_mode=ParseMode.HTML)

    await json_file_handler.save_command(command=data["command"], description=data["description"])
    await state.clear()

@admin.message(Command("remove"))
async def cmd_remove(message: Message, state: FSMContext) -> None:
    data = await json_file_handler.load_commands()

    if not data:
        await message.answer("Нет доступных команд.")
        return

    commands_list = "\n\n".join([f"<b>Команда:</b> {cmd_data['command']}\n"
                                 f"<b>Описание:</b> {cmd_data['description']}"
                                 for cmd_data in data.values()])

    await message.answer(f"Доступные команды:\n\n{commands_list}")

    await message.answer("Напишите название команды, которую хотите удалить, без «/»\n"
                         "/cancel для отмены удаления команды")
    await state.set_state(CommandState.delete_command)

@admin.message(Command("cancel"), CommandState.delete_command)
async def cancel_delete_process(message: Message, state: FSMContext) -> None:
    await message.answer("Удаление команды отменено.")
    await state.clear()

@admin.message(CommandState.delete_command)
async def del_command(message: Message, state: FSMContext) -> None:
    data = await json_file_handler.load_commands()

    command_exists = False

    for cmd_data in data.values():
        if cmd_data['command'] == f"/{message.text}":
            command_exists = True
            await json_file_handler.delete_command(cmd_data['command'])
            await message.answer(f"Команда {cmd_data['command']} <b>успешно удалена!</b>")
            await state.clear()
            break

    if not command_exists:
        await message.answer("Введена не существующая команда.\n"    
                             "Попробуйте еще раз!\n")