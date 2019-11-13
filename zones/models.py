from django.db import models

# Create your models here.
from zones.managers import DestinationManager


class Country(models.Model):
    place = models.CharField(max_length=100, unique=True, null=True, blank=True)
    objects = DestinationManager()

    def __str__(self):
        return str(self.place)

    class Meta:
        db_table = 'destinations'
        verbose_name = 'Destino'
        verbose_name_plural = 'Destinos'