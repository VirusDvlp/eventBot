from aiogram.fsm.state import State, StatesGroup


class NewOrganizerFSM(StatesGroup):
    contactState = State()
    nameState = State()
