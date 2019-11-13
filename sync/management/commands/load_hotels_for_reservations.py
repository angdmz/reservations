from django.core.management.base import BaseCommand
import logging

from reservations.models import Reservation
from sync.services import generate_reservations_updater, generate_hotel_loader
from zones.models import Country

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    country_manager = Country.objects
    updater = generate_reservations_updater()
    hotel_loader = generate_hotel_loader()
    reservation_manager = Reservation.objects

    def handle(self, *args, **options):
        all_reservations = self.reservation_manager.all()
        places = [reservation.destination for reservation in all_reservations]
        self.stdout.write("Updating hotels for places")
        hotels = self.hotel_loader.load_hotels_for_destinations(places)
        self.stdout.write("Hotels loaded for places, count: {}".format(len(hotels)))