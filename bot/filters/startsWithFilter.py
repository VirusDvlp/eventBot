from aiogram import types
from aiogram.filters import Filter


class StartsWithFilter(Filter):
    def __init__(self, text: str):
        self.text = text

    async def __call__(self, data):
        input_text = data.text if isinstance(data, types.Message) else data.data
        return input_text.startswith(self.text)
