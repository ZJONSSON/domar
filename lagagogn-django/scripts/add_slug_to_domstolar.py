from django.utils.text import slugify


from domar.models import Domstoll


def run():
    for obj in Domstoll.objects.all():
        if not obj.slug:
            slug = slugify(obj.name)
            obj.slug = slug
            obj.save()
