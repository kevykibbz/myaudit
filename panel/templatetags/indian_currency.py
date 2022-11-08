from django import template
from django.utils.translation import to_locale,get_language
from babel.numbers import format_currency

register=template.Library()

@register.filter
def indian_currency(number,locale=None):
    if locale is None:
        locale=to_locale(get_language())
        s, *d = str(number).partition(".")
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        #return format_currency(number,'INR',locale=locale)
        return "".join([r] + d)
