from django.contrib import admin

from .models import Domstoll, Domur


class DomurAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'domstoll', 'date', 'tags')

admin.site.register(Domstoll)
admin.site.register(Domur, DomurAdmin)
