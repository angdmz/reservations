from django.db import models

# Create your models here.
from reservations.managers import ReservationManager
from zones.models import Country


class Reservation(models.Model):
    date = models.DateTimeField()
    destination = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=4+8+4+4+4+12)
    objects = ReservationManager()

    def __str__(self):
        return "external id: {} ; destination: {} ; date: {}"\
            .format(str(self.external_id),str(self.destination), str(self.date))

    class Meta:
        db_table = 'reservations'
        verbose_name = 'Reservacion'
        verbose_name_plural = 'Reservaciones'
