from django import template
import os
register=template.Library()


@register.filter(name='sampler')
def sampler(data,args):
    if data is not None:
        return (data[:18] + '...<a href="#largeModel_%s" data-toggle="modal" data-target="#largeModel_%s">see more</a>' %(str(args),str(args)))  if len(data) > 60 else data
