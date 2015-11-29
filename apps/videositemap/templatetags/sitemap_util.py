from django import template

register = template.Library()


@register.filter
def sec_to_min(value):
    return int(value) / 60
