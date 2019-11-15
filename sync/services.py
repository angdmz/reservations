import collections
import json
import logging

import requests
from django.conf import settings

from hotels.models import Hotel
from reservations.models import Reservation
from sync.exceptions import EmptyCityNameException, InvalidParametersException, FourSquareApiException
from zones.models import Country as Destination, Country

logger = logging.getLogger(__name__)

class HotelSearcher:

    def __init__(self, venue_repository):
        self.venue_repository = venue_repository

    def search_hotels_by_city(self, city_name):
        if city_name == '':
            raise EmptyCityNameException('No city name given')
        try:
            logger.info("Searching cities")
            venues = self.venue_repository.get_venues(city_name, 'browse', 'hotels')
        except InvalidParametersException as ipe:
            return []
        return venues['response']['venues']


def generate_hotel_searcher():
    api_consumer = FourSquareApiConsumer(settings.FOURSQUARE_API_ENDPOINT,
                                         settings.FOURSQUARE_API_CLIENT_ID,
                                         settings.FOURSQUARE_API_CLIENT_SECRET,
                                         settings.FOURSQUARE_API_VERSION)
    return HotelSearcher(api_consumer)


class FourSquareApiConsumer:

    def __init__(self, endpoint_url, client_id, client_secret, version):
        self.version = version
        self.endpoint_url = endpoint_url
        self.client_secret = client_secret
        self.client_id = client_id


    def get_venues(self, near, intent, query):
        params = {'near': near,
                  'intent':intent,
                  'query':query,
                  'client_id': self.client_id,
                  'client_secret': self.client_secret,
                  'v': self.version}
        logger.debug("Requesting to {} with params {}".format(str(self.endpoint_url), str(params)))
        res = requests.get(self.endpoint_url, params)

        decoded_response = json.loads(res.content.decode())
        if 0 <= res.status_code - 400 <= 12:
            raise InvalidParametersException('Client side error, status code: {} ; error detail: {}'
                                             .format(str(res.status_code),
                                                     str(decoded_response['meta']['errorDetail'])))
        if 0 <= res.status_code - 500 <= 12:
            logger.error("Request to {} with params {} responded server side error with {}, message: {}"
                         .format(str(self.endpoint_url), str(params), str(res.status_code), str(decoded_response['meta']['errorDetail'])))
            raise FourSquareApiException(decoded_response['meta']['errorDetail'])

        return decoded_response

    
class ReservationsRetriever:

    def __init__(self, endpoint_url,):
        self.endpoint_url = endpoint_url

    def retrieve_recent_reservations(self):
        res = requests.get(self.endpoint_url)
        if 0 <= res.status_code - 500 <= 12:
            logger.error("Endpoint {} responsed with {} and response {}, returning empty response for this method"
                         .format(self.endpoint_url, res.status_code, str(res.content.decode())))
            return []
        if 0 <= res.status_code - 400 <= 12:
            raise InvalidParametersException('Client side error, status code: {} ; error detail: {}'
                                             .format(str(res.status_code), str(res.content.decode())))
        decoded_response = json.loads(res.content.decode())

        ReservationStruct = collections.namedtuple('ReservationStruct', 'date destination reservation_id')
        res = [
            ReservationStruct(date=d['date'], destination=d['destination'], reservation_id=d['reservationId'])
            for d in decoded_response]
        return res


def generate_reservations_retriever():
    return ReservationsRetriever(settings.RESERVATIONS_ENDPOINT)


class ReservationsUpdater:

    reservation_manager = Reservation.objects
    destination_manager = Destination.objects

    def __init__(self, reservations_retriever):
        self.reservations_retriever = reservations_retriever

    def update_reservations(self):
        logger.info("Starting update reservations")
        recent_reservations = self.reservations_retriever.retrieve_recent_reservations()
        dest_list = [
            Destination(place=r.destination)
            for r in recent_reservations
        ]
        created_destinations = self.destination_manager.bulk_destinations(dest_list)
        dict_destinations = {d.place: d for d in created_destinations}
        reservations_list = [
            Reservation(destination=dict_destinations[r.destination], date=r.date, external_id=r.reservation_id)
            for r in recent_reservations
        ]
        created_objs = self.reservation_manager.bulk_reservations(reservations_list)
        logger.info("Update process finished")
        return len(recent_reservations) is not 0, created_objs


def generate_reservations_updater():
    return ReservationsUpdater(generate_reservations_retriever())


class HotelLoader:

    hotel_manager = Hotel.objects
    places_manager = Country.objects

    def __init__(self, hotel_searcher):
        self.hotel_searcher = hotel_searcher

    def load_hotels_for_destinations(self, destinations):
        hotels = []
        logger.info("Loading hotels for {} destinations given".format(len(destinations)))
        for destination in destinations:
            logger.debug("Loading destination {}".format(str(destination)))
            hotels_search_result = self.hotel_searcher.search_hotels_by_city(destination.place)
            hotels_for_place = \
                [
                    Hotel(name=hotel['name'], zone=destination,
                          address=hotel['location'].get('address',hotel['location']['formattedAddress'][0]))
                    for hotel in hotels_search_result
                ]
            hotels.extend(hotels_for_place)
        logger.debug("Bulking hotels")
        logger.info("Loading finished")
        return self.hotel_manager.bulk_create(hotels, ignore_conflicts=True)


def generate_hotel_loader():
    return HotelLoader(generate_hotel_searcher())
