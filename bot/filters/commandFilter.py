from aiogram import types
from aiogram.filters import Filter


class CommandFilter(Filter):
    def __init__(self, command: str):
        self.command = command

    async def __call__(self, m: types.Message):
        return m.text == '/' + self.command
