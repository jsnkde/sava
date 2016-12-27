from django import template
from django.conf import settings
from catalog.models import Location

register = template.Library()

@register.filter()
def region_to_str(value):
    return Location.REGIONS[int(value)][1]
    
# @register.filter()
# def add(value, number):
# 	return value + number

@register.filter()
def addcss(field, css):
   return field.as_widget(attrs={"class": css})

@register.filter()
def can_give_karma(field, owner):
   return field.can_give_karma(owner)

@register.filter()
def to_str(field):
   return unicode(field)

@register.filter()
def range(val):
   return xrange(val)

@register.filter()
def concat(str1, str2):
   return (unicode(str1) + unicode(str2))

@register.filter()
def img_selector(field, val):
   return field.as_widget(attrs={"onchange": 'get_file_name("{}");'.format(val), "class": "hidden"})

@register.simple_tag
def get_setting(name):
    return getattr(settings, name, "")