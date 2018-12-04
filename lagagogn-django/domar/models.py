from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils.text import slugify


class Domstoll(models.Model):
    name = models.CharField(max_length=128, verbose_name="nafn")
    url = models.CharField(max_length=255, verbose_name="slóð")


    class Meta:
        verbose_name = 'Dómstóll'
        verbose_name_plural = 'Dómstólar'

    def __str__(self):
        return self.name


class Domur(models.Model):
    identifier = models.CharField(max_length=20, unique=True)
    domstoll = models.ForeignKey(Domstoll, on_delete=models.CASCADE, verbose_name="dómstóll")
    parties = models.TextField(blank=True)
    appellants = models.TextField(blank=True)
    plaintiffs = models.TextField(blank=True)
    judge = models.CharField(max_length=255, blank=True, default="")
    date = models.DateField()
    tags = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    abstract = models.TextField(blank=True)
    text = models.TextField(blank=True)
    url = models.CharField(max_length=255, blank=False, default="")
    slug = models.SlugField(max_length=100, default="")

    class Meta:
        verbose_name = 'Dómur'
        verbose_name_plural = 'Dómar'

    def __str__(self):
        return " - ".join((self.domstoll.name, self.identifier))

    def get_absolute_url(self):
        return reverse('domur',
            args=[str(slugify(self.domstoll.name,
                allow_unicode=True)),
            self.slug])


    def has_text(self):
        if self.text:
            return True
        return False
    has_text.boolean = True
    has_text.short_description = 'Dómtexti'
