from aiogram.fsm.state import State, StatesGroup

class CommandState(StatesGroup):
    command = State()
    description = State()
    delete_command = State()