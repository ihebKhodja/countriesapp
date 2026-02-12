from django.db import models

# Create your models here.
class Country(models.Model):
    cca3 = models.CharField(max_length=3, unique=True)
    common_name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255)
    native_name = models.JSONField(blank=True, null=True)
    cca2 = models.CharField(max_length=2, unique=True)
    capital = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    subregion = models.CharField(max_length=255, blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    flag_url = models.URLField(blank=True, null=True)
    currencies = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.common_name