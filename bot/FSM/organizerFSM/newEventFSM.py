from aiogram.fsm.state import State, StatesGroup


class NewEventFSM(StatesGroup):
    titleState = State()
    descrState = State()
    datetimeState = State()
    addressState = State()
    membersNumberState = State()
    priceState = State()
    payTypeState = State()
    requisitesState = State()
