from django.contrib import admin

from .models import User, Location, Item

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Location)
