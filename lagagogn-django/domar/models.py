from django.db import models
from django.contrib.postgres.fields import ArrayField


class Domstoll(models.Model):
    name = models.CharField(max_length=128, verbose_name="nafn")
    url = models.CharField(max_length=255, verbose_name="slóð")

    class Meta:
        verbose_name = 'Dómstóll'
        verbose_name_plural = 'Dómstólar'

    def __str__(self):
        return self.name


class Domur(models.Model):
    identifier = models.CharField(max_length=20)
    domstoll = models.ForeignKey(Domstoll, on_delete=models.CASCADE, verbose_name="dómstóll")
    parties = models.CharField(max_length=255, blank=False, default="")
    appellants = models.CharField(max_length=255, blank=False, default="")
    plaintiffs = models.CharField(max_length=255, blank=False, default="")
    date = models.DateField()
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    abstract = models.TextField(blank=True)
    text = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Dómur'
        verbose_name_plural = 'Dómar'

    def __str__(self):
        return " - ".join((self.domstoll.name, self.identifier))
