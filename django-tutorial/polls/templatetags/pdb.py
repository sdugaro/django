from django.conf import settings
from django import template

register = template.Library()


@register.filter
def pdb(element, enable="on"):
    if settings.DEBUG:
        if enable.lower() in ['on', 'true']:
            breakpoint()
    return element


@register.simple_tag(takes_context=True)
def set_breakpoint(context):
    if settings.DEBUG:
        breakpoint()
