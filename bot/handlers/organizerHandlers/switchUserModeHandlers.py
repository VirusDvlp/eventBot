from aiogram import types, Dispatcher

from createBot import db, ADMIN_ID

import keyboards as kb
import filters as f


async def switch_to_user(m: types.Message):
    organizer = m.from_user.id
    db.switch_user_mode(organizer, 1)
    await m.answer(
        '''Теперь вы можете пользоваться ботом, как клиент, чтобы начать это, введите команду /start
Чтобы переключиться обратно в режим организатор воспользуйтесь командой - /switchusermode''',
        reply_markup=types.ReplyKeyboardMarkup(keyboard=[[]])
    )


async def switch_to_organizer(m: types.Message):
    if db.get_organizer_data(m.from_user.id):
        db.switch_user_mode(m.from_user.id, 0)
        if m.from_user.id in ADMIN_ID:
            await m.answer('Вы успешно переключились на режим администратор', reply_markup=kb.main_admin_kb)
        else:
            await m.answer('Вы успешно переключились на режим организатора', reply_markup=kb.main_organizer_kb)


def register_switch_user_mode_handlers(dp: Dispatcher):
    dp.message.register(switch_to_user, f.CommandFilter('switchusermode'), f.Or(f.OrganizerFilter(), f.AdminFilter()))
    dp.message.register(switch_to_organizer, f.CommandFilter('switchusermode'))
