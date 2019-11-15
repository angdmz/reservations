from django.db import models


class HotelManager(models.Manager):
    def find_hotels_by_place(self, place):
        # suuuper inefficient
        return self.filter(zone__place__icontains=place)


