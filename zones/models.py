from django.db import models

# Create your models here.

class Country(models.Model):
    place = models.CharField(max_length=100)

    class Meta:
        db_table = 'countries'
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'