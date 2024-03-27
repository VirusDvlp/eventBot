from .newEventHandlers import register_new_event_handlers
from .showEventsDataHandlers import register_show_events_data_handlers
from .mainOrganizerHandlers import register_main_admin_handlers
from .buyTicketHandlers import register_buy_ticket_handlers
from .switchUserModeHandlers import register_switch_user_mode_handlers


def register_organizer_handlers(dp):
    register_main_admin_handlers(dp)
    register_new_event_handlers(dp)
    register_show_events_data_handlers(dp)
    register_buy_ticket_handlers(dp)
    register_switch_user_mode_handlers(dp)
