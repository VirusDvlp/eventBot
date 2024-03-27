from aiogram import types, Dispatcher

from createBot import db

import keyboards as kb
import filters as f


async def verify_pay(c: types.CallbackQuery):
    ticket = c.data.split('_')[1]
    ticket_info = db.get_ticket_info(ticket)
    if ticket_info['status'] == 1:
        db.verify_ticket(ticket)
        ref_info = db.get_referal_data(ticket_info['user_id'])
        if ref_info['referal_to']:
            db.plus_bonus(ref_info['referal_to'], int(ticket_info['price'] * 0.05))
        await c.bot.send_message(
            chat_id=int(ticket_info['user_id']),
            text=f'Ваш билет на {ticket_info["datetime"]} - {ticket_info["title"]}. Подтверждён'
        )
        await c.answer('Покупка билета успешно подтверждена')
    else:
        await c.message.delete_reply_markup()
        await c.answer('На данное мероприятие уже не продаются билеты')


async def cancel_verify(c: types.CallbackQuery):
    ticket = c.data.split('_')[1]
    ticket_info = db.get_ticket_info(ticket)
    if ticket_info:
        db.delete_ticket(ticket)
        await c.bot.send_message(int(ticket_info['user_id']), 'Ваша оплата билета отклонена продавцом')
        await c.answer('Заявка успешно отклонена')
    else:
        await c.answer()


def register_buy_ticket_handlers(dp: Dispatcher):
    dp.callback_query.register(verify_pay, f.StartsWithFilter('verify_'), f.Or(f.AdminFilter(), f.OrganizerFilter()))
    dp.callback_query.register(cancel_verify, f.StartsWithFilter('unverify_'), f.Or(f.AdminFilter(), f.OrganizerFilter()))
