from django.db import models

# Create your models here.

class Reservation(models.Model):
    date = models.DateTimeField()
    destination = models.DateTimeField()