from django.contrib import admin
from django.db.models import Count

from .models import Domstoll, Domur

from django.utils.translation import gettext_lazy as _


def has_attribute_filter(has_attribute):
    class GenericDomurHasListFilter(admin.SimpleListFilter):

        function = getattr(Domur, has_attribute)
        title = _(function.short_description)
        parameter_name = function.parameter_name

        def lookups(self, request, model_admin):
            return (
                ('false', _('Vantar')),
                ('true', _('Til staðar')),
            )

        def queryset(self, request, queryset):
            if self.value() == 'false':
                missing = [x.id for x in queryset if not getattr(x, has_attribute)()]
                return queryset.filter(pk__in=missing)
            if self.value() == 'true':
                exists = [x.id for x in queryset if getattr(x, has_attribute)()]
                return queryset.filter(pk__in=exists)

    return GenericDomurHasListFilter


has_attributes = ['has_text', 'has_parties', 'has_appellants', 'has_plaintiffs', 'has_judge', 'has_abstract']
domur_has_list_filters = []
for has_attribute in has_attributes:
    domur_has_list_filters.append(has_attribute_filter(has_attribute))


class DomurAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'domstoll', 'date', 'tags'] + has_attributes
    list_filter = ['domstoll'] + domur_has_list_filters


class DomstollAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(DomstollAdmin, self).get_queryset(request)
        return qs.annotate(domar_count=Count('domur'))

    def domar_count(self, inst):
        return inst.domar_count

    domar_count.short_description = 'Fjöldi dóma'

    list_display = ('name', 'domar_count')
    list_filter = ('name',)

    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Domstoll, DomstollAdmin)
admin.site.register(Domur, DomurAdmin)
