from django.contrib import admin
from django.db.models import Count

from .models import Domstoll, Domur


class DomurAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'domstoll', 'date', 'tags')
    list_filter = ('domstoll',)

class DomstollAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(DomstollAdmin, self).get_queryset(request)
        return qs.annotate(domar_count=Count('domur'))

    def domar_count(self, inst):
        return inst.domar_count

    list_display = ('name', 'domar_count')
    list_filter = ('name',)

admin.site.register(Domstoll, DomstollAdmin)
admin.site.register(Domur, DomurAdmin)
