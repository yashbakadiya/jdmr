from django import template

register = template.Library()
@register.filter
def getid(value,arg):
    return str(arg)+str(value)
