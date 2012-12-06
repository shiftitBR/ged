from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('twain/dynamictwain.html')
def digitalizacao():
    return {}
