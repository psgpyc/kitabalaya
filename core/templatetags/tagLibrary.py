from django import template

register = template.Library()


@register.filter()
def to_int(value):
    if type(value) == str:
        return value
    else:
        return int(value)