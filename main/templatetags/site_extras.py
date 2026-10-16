import re

from django import template

register = template.Library()


@register.filter
def phone_digits(value):
    """'+996 (507) 02-22-02' -> '996507022202' — для ссылок tel: и wa.me."""
    return re.sub(r'\D', '', str(value or ''))
