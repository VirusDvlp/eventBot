from aiogram import types
from aiogram.filters import Filter

from createBot import ADMIN_ID, db


class AdminFilter(Filter):
    async def __call__(self, data):
        if not data.from_user.id in ADMIN_ID:
            return False
        admin_info = db.get_organizer_data(data.from_user.id)
        return admin_info.get('is_user', False) == 0
