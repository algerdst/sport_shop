from django import template

register = template.Library()


@register.filter(name='range')
def create_range(value, start_index=0):
    return range(start_index, value + start_index)


@register.filter(name='sub')
def subtract(value, arg):
    return value - arg
