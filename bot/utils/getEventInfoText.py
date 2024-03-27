from jinja2 import Template


def get_event_info_text(event_info: dict, is_for_organizer=True) -> str:
    tmplt = """
{{ event_info['title'] }}

Дата, время: {{ event_info['datetime'] }}

{{ event_info['descr'] }}

Адрес: {{ event_info['address'] }}
Участники: {{ event_info['members'] }} из {{ event_info['members_number'] }}

Стоимость билета: {{ event_info['ticket_price'] }}
Тип оплаты: {% if event_info['pay_type'] == 1 %}на мероприятии{%else%}онлайн{% endif %}
{% if is_for_organizer %}{% if event_info['pay_type'] == 0%}Реквизиты для оплаты:\n{{ event_info['requisites'] }}{% endif %}
Организатор - {{ event_info['org_name'] }}{% endif %}
"""
    return Template(tmplt).render(event_info=event_info, is_for_organizer=is_for_organizer)
