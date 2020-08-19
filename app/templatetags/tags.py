from django import template
from django.utils.timezone import now

register = template.Library()


@register.simple_tag
def time_now():
    return now()
