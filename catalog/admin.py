from django.contrib import admin

from .models import User, Location, Item, Karma, Image
from sorl.thumbnail.admin import AdminImageMixin


class ImageInline(AdminImageMixin, admin.TabularInline):
    model = Image

class ItemAdmin(admin.ModelAdmin):
    inlines = [ ImageInline, ]


admin.site.register(User)
admin.site.register(Karma)
admin.site.register(Item, ItemAdmin)
admin.site.register(Location)
admin.site.register(Image)