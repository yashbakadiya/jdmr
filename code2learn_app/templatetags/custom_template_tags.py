from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.simple_tag
def setvar(val=None):
    return val


@register.filter(name="first_name")
def get_first_name(name):
    return name.split(" ")[0]


@register.filter(name="remove_space")
def remove_space(value):
    return str(value).replace(" ", "")


@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]


upto.is_safe = True
