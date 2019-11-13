from django.db import models


class ReservationManager(models.Manager):

    def find_reservation_by_id(self, reservation_id):
        return self.get(reservation_id=reservation_id)

    def bulk_reservations(self, reservations_list):
        return self.bulk_create(reservations_list)

    def exists_reservation_with_id(self, reservation_id):
        return self.filter(reservation_id=reservation_id)
