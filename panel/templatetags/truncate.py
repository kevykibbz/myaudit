from django import template
import os
register=template.Library()


@register.filter(name='truncate')
def truncate(data):
    if data is not None:
       	return (data[:18] + '...<a href="#largeModel" data-toggle="modal" data-target="#largeModel">see more</a>') if len(data) > 60 else data
