from django.db import models

# Create your models here.
from zones.models import Country


class Reservation(models.Model):
    date = models.DateTimeField()
    destination = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=4+8+4+4+4+12)

    class Meta:
        db_table = 'reservations'
        verbose_name = 'Reservacion'
        verbose_name_plural = 'Reservaciones'