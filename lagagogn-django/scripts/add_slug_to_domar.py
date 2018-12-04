from django.utils.text import slugify


from domar.models import Domur


def run():
    for obj in Domur.objects.all():
        if not obj.slug:
            slug = slugify(obj.identifier)
            obj.slug = slug
            obj.save()
