from django import template
from catalog.models import Location

register = template.Library()

@register.filter()
def region_to_str(value):
    return Location.REGIONS[int(value)][1]
    