import re

from django import template

from main.models import PageHero

register = template.Library()


@register.filter
def phone_digits(value):
    """'+996 (507) 02-22-02' -> '996507022202' — для ссылок tel: и wa.me."""
    return re.sub(r'\D', '', str(value or ''))


@register.simple_tag
def page_hero(page):
    """Заголовок и подзаголовок страницы из админки (или None)."""
    return PageHero.objects.filter(page=page).first()
