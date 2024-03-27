from aiogram.fsm.state import State, StatesGroup


class EditBotDataFSM(StatesGroup):
    valueState = State()
