from django import template
import os
register=template.Library()


@register.filter(name='filename')
def filename(data):
    if data is not None:
       	return os.path.basename(data.file.name)
