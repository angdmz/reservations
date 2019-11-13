from django.db import models


class DestinationManager(models.Manager):

    def bulk_destinations(self, destinations):
        #ignore_conflicts only works with postgres!!
        self.bulk_create(destinations, ignore_conflicts=True)
        return self.filter(place__in=destinations)

    def exists_place(self, place):
        return self.filter(place=place).exists()
