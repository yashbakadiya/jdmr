from django import template

register = template.Library()
@register.filter
def splitspace(value):
    return value.split(" ")
