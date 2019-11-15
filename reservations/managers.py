from django.db import models


class ReservationManager(models.Manager):

    def find_reservation_by_id(self, reservation_id):
        return self.get(external_id=reservation_id)

    def bulk_reservations(self, reservations_list):
        return self.bulk_create(reservations_list)

    def exists_reservation_with_id(self, reservation_id):
        return self.filter(external_id=reservation_id).exists()

    def find_reservations_by_destination(self, destination):
        # waaaay inefficient
        return self.filter(destination__place__icontains=destination).order_by('date')