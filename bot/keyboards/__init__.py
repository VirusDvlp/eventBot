from .adminKb.mainAdminKb import main_admin_kb, edit_bot_data_kb
from .adminKb.editOrganizersKb import req_contact_kb, get_list_of_organizers_kb

from .organizerKb.eventManagementKb import pay_type_kb, get_event_list_kb, get_org_event_info_kb
from .organizerKb.buyTicketsKb import get_verify_pay_kb
from .organizerKb.mainOrganizerKb import main_organizer_kb

from .userKb.mainUserKb import main_user_kb, request_phone_kb, edit_user_data_kb, sub_on_channel_kb
from .userKb.showEventKb import get_event_info_kb, get_i_paid_kb
from .userKb.showTicketsKb import get_tickets_list_kb

from .toMenuKb import go_to_menu_kb, go_to_menu_reply_kb
