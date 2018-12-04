from django.contrib.syndication.views import Feed
from django.urls import reverse
from domar.models import Domur


class LatestDomar(Feed):
    title = "Lagagögn - dómar"
    link = "/domar/"
    description = "Nýjustu dómarnir frá dómstólum"

    def items(self):
        return Domur.objects.order_by('-date')[:20]

    def item_title(self, item):
        return item

    def item_description(self, item):
        return item.abstract

    #def item_link(self, item):
    #    return item.url
        #return reverse('domur', args=[item.pk])
