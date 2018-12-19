from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils.text import slugify


class Domstoll(models.Model):
    name = models.CharField(max_length=128, verbose_name="nafn")
    url = models.CharField(max_length=255, verbose_name="slóð")
    slug = models.SlugField(max_length=100, default="")

    class Meta:
        verbose_name = 'Dómstóll'
        verbose_name_plural = 'Dómstólar'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('domstoll', args=[self.slug])


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
        return reverse('domur', args=[self.domstoll.slug, self.slug])

    def has_text(self):
        if self.text:
            return True
        return False
    has_text.boolean = True
    has_text.short_description = 'Dómtexti'
    has_text.parameter_name = 'text'

    def has_parties(self):
        if self.parties:
            return True
        return False
    has_parties.boolean = True
    has_parties.short_description = 'Aðilar'
    has_parties.parameter_name = 'parties'

    def has_appellants(self):
        if self.appellants:
            return True
        return False
    has_appellants.boolean = True
    has_appellants.short_description = 'Stefnandi'
    has_appellants.parameter_name = 'appellants'

    def has_plaintiffs(self):
        if self.plaintiffs:
            return True
        return False
    has_plaintiffs.boolean = True
    has_plaintiffs.short_description = 'Stefndi'
    has_plaintiffs.parameter_name = 'plaintiffs'

    def has_judge(self):
        if self.judge:
            return True
        return False
    has_judge.boolean = True
    has_judge.short_description = 'Dómari'
    has_judge.parameter_name = 'judge'

    def has_abstract(self):
        if self.abstract:
            return True
        return False
    has_abstract.boolean = True
    has_abstract.short_description = 'Reifun'
    has_abstract.parameter_name = 'abstract'
