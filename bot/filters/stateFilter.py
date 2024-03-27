from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter


class StateFilter(Filter):
    def __init__(self, state):
        self.state = state

    async def __call__(self, message, state: FSMContext):
        if self.state == '*':
            return True
        else:
            return self.state == await state.get_state()
