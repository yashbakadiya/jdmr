from django import template

register = template.Library()
@register.filter
def n2comma(value):
    return str(value).replace("\n",", ")
