from django.contrib import admin

from .models import User, Location, Item, Karma

admin.site.register(User)
admin.site.register(Karma)
admin.site.register(Item)
admin.site.register(Location)
