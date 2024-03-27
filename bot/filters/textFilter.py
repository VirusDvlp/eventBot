from aiogram import types
from aiogram.filters import Filter


class TextFilter(Filter):
    def __init__(self, text: str):
        self.text = text

    async def __call__(self, data):
        data = data.text if isinstance(data, types.Message) else data.data
        return self.text == data
