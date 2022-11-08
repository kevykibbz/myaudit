from django import template
import json
import validators
register=template.Library()

@register.filter(name='decoder')
def decoder(data):
    if data is not None and len(data) > 0:
        jsonDec=json.decoder.JSONDecoder()
        joined_string=",".join(jsonDec.decode(data))
        return joined_string
    else:
        return 'Not Set'
      
      
