from django import template
from datetime import date
register=template.Library()

@register.filter(name='due')
def due(data):
    if data:
        today=date.today()
        return data-today
