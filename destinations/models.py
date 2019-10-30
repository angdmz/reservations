from django.db import models

# Create your models here.

class Destination(models.Model):
    place = models.CharField(max_length=100)