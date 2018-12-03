from django.contrib import admin
from django.db.models import Count

from .models import Domstoll, Domur

from django.utils.translation import gettext_lazy as _


class DomurHasTextListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Dómtexti')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'text'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('false', _('Vantar')),
            ('true', _('Til staðar')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'false':
            missing = [x.id for x in queryset if not x.has_text()]
            return queryset.filter(pk__in=missing)
        if self.value() == 'true':
            exists = [x.id for x in queryset if x.has_text()]
            return queryset.filter(pk__in=exists)




class DomurAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'domstoll', 'date', 'tags', 'has_text')
    list_filter = ('domstoll', DomurHasTextListFilter)


class DomstollAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(DomstollAdmin, self).get_queryset(request)
        return qs.annotate(domar_count=Count('domur'))

    def domar_count(self, inst):
        return inst.domar_count

    domar_count.short_description = 'Fjöldi dóma'

    list_display = ('name', 'domar_count')
    list_filter = ('name',)

admin.site.register(Domstoll, DomstollAdmin)
admin.site.register(Domur, DomurAdmin)
