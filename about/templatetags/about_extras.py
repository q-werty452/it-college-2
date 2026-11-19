from django import template
from django.utils.safestring import mark_safe

from about.icons import ICONS

register = template.Library()


@register.filter
def svg_icon(key):
    """Возвращает внутренности <svg> для выбранной в админке иконки."""
    return mark_safe(ICONS.get(key, ICONS["check"]))
