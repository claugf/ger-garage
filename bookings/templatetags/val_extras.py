
from django import template

register = template.Library()


@register.filter(name='upper')
# Validating text format, only Uppercase
def upper(value):
    return value.upper()
