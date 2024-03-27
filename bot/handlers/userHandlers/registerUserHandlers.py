from .mainUserHandlers import register_main_user_handlers
from .showEventsHandlers import register_show_events_data_handlers
from .buyTicketHandlers import register_buy_ticket_handlers
from .editUserDataHandlers import register_edit_user_data_handlers
from .referalSystemHandlers import register_referal_system_handlers
from .historyOfTicketsHandlers import register_show_tickets_data_handlers


def register_user_handlers(dp):
    register_main_user_handlers(dp)
    register_show_events_data_handlers(dp)
    register_buy_ticket_handlers(dp)
    register_edit_user_data_handlers(dp)
    register_referal_system_handlers(dp)
    register_show_tickets_data_handlers(dp)
