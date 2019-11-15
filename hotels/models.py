from django.db import models

# Create your models here.
from hotels.managers import HotelManager
from zones.models import Country as Destination


class Hotel(models.Model):
    zone = models.ForeignKey(Destination, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    objects = HotelManager()

    def __str__(self):
        return "{} {}".format(str(self.name), str(self.zone))

    class Meta:
        db_table = 'hotels'
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hoteles'
        unique_together = ('name', 'zone')