from django import template
register = template.Library()

@register.filter(name='in')
def inside(value, arg):
    return value in arg