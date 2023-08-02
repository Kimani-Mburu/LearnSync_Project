# learnsyc_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def has_extension(value, extension):
    if value and value.name:
        return value.name.lower().endswith(extension.lower())
    return False
