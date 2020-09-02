from django import template

register = template.Library()
@register.filter
def leftdate(value):
    return str(value).split(",")[0]

@register.filter
def rightdate(value):
    return str(value).split(",")[1]
