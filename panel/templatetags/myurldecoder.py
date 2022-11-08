from django import template
import json
import urllib

register=template.Library()


@register.filter(name='myurldecoder')
def myurldecoder(data):
    if data is not None:
       	jsonDec=json.decoder.JSONDecoder()
        joined_string=jsonDec.decode(urllib.parse.unquote(str(data)))
        return joined_string
      
