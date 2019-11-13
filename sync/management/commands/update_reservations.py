from django.core.management.base import BaseCommand
import logging

from sync.services import generate_reservations_updater, generate_hotel_loader
from zones.models import Country

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    country_manager = Country.objects
    updater = generate_reservations_updater()
    hotel_loader = generate_hotel_loader()

    def handle(self, *args, **options):
        self.stdout.write("Updating reservations")
        updated, new_reservations = self.updater.update_reservations()
        self.stdout.write(
            "Updated reservations? {}, new reservations count: {}"
                .format(str(updated), str(len(new_reservations)))
        )
        places = [reservation.destination for reservation in new_reservations]
        self.stdout.write("Updating hotels for places")
        hotels = self.hotel_loader.load_hotels_for_destinations(places)
        self.stdout.write("Hotels loaded for places, count: {}".format(len(hotels)))