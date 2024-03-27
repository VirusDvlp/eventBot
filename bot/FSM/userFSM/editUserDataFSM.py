from aiogram.fsm.state import State, StatesGroup


class EditUserDataFSM(StatesGroup):
    valueState = State()
