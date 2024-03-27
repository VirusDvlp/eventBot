from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import create_start_link

from jinja2 import Template

from createBot import db

import filters as f


async def show_referal_data(m: types.Message):
    ref_info = db.get_referal_data(m.from_user.id)
    await m.answer(
        text=Template('''Ваша реферальная ссылка - {{ link }}
У вас бонусов на счету: {{ bonus }}
Люди зарегистрировашиеся по вашей реферальной ссылке:
{% for ref in referals %}- {{ ref["name"] }} @{{ ref["username"] }}{% endfor %}
''').render(
            link=await create_start_link(m.bot, str(m.from_user.id), encode=True),
            bonus=ref_info["bonus"],
            referals=ref_info['referals']
        )
    )


def register_referal_system_handlers(dp: Dispatcher):
    dp.message.register(show_referal_data, f.TextFilter('Реферальная система'))
