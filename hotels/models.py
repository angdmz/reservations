from django.db import models

# Create your models here.
from zones.models import *


class Hotel(models.Model):
    zone = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'hotels'
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hoteles'