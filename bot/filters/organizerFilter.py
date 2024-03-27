from aiogram import types
from aiogram.filters import Filter

from createBot import db


class OrganizerFilter(Filter):
    async def __call__(self, data):
        org_info = db.get_organizer_data(data.from_user.id)
        if not org_info:
            return org_info
        else:
            return org_info['is_user']
