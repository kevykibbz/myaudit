from django import template

register=template.Library()

@register.filter
def trimmer(value):
    if value is not None:
       return value.split('d')[0]
