from django import template

register = template.Library()
@register.filter
def semicolontohtml(value):
    return str(value).replace(";","<br>")
