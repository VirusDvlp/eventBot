from .mainAdminHandlers import register_main_admin_handlers
from .newOrganizerHandlers import register_new_organizer_handlers
from .showOrganizersDataHandlers import register_show_organizers_data_handlers
from .showEventsDataHandlers import register_show_events_data_handlers
from .editBotDataHandlers import register_edit_bot_data_handlers


def register_admin_handlers(dp):
    register_main_admin_handlers(dp)
    register_new_organizer_handlers(dp)
    register_show_organizers_data_handlers(dp)
    register_show_events_data_handlers(dp)
    register_edit_bot_data_handlers(dp)
