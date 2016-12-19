from django import template
from catalog.models import Location

register = template.Library()

@register.filter()
def region_to_str(value):
    return Location.REGIONS[int(value)][1]
    

@register.filter()
def add(value, number):
	return value + number

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})
   