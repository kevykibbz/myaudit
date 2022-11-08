from django import template
import json
register=template.Library()

@register.filter(name='ranger')
def ranger(data):
    if data is not None:
       return range(int(data))
      
