from aiogram import types
from aiogram.filters import Filter


class ContentTypeFilter(Filter):
    def __init__(self, content_type: str):
        self.content_type = content_type

    async def __call__(self, m: types.Message):
        return m.content_type == self.content_type
