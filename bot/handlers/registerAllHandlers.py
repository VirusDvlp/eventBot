from .adminHandlers import register_admin_handlers
from .organizerHandlers import register_organizer_handlers
from .userHandlers import register_user_handlers
from .extraHandlers import register_extra_handlers


def register_all_handlers(dp):
    register_admin_handlers(dp)
    register_organizer_handlers(dp)
    register_user_handlers(dp)
    register_extra_handlers(dp)
