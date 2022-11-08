from django import template

register=template.Library()

@register.filter
def initials(value):
    if value is not None:
       return value.split(' ')[0][0].upper()
