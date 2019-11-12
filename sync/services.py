import json

import requests
from django.conf import settings


class EmptyCityNameException(Exception):
    pass


class HotelSearcher:

    def __init__(self, venue_repository):
        self.venue_repository = venue_repository

    def search_hotels_by_city(self, city_name):
        if city_name == '':
            raise EmptyCityNameException('No city name given')
        try:
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


class InvalidParametersException(Exception):
    pass


class FourSquareApiException(Exception):
    pass


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
        res = requests.get(self.endpoint_url, params)
        decoded_response = json.loads(res.content.decode())
        if 0 <= res.status_code - 400 <= 12:
            raise InvalidParametersException('Client side error, status code: {} ; error detail: {}'
                                             .format(str(res.status_code),
                                                     str(decoded_response['meta']['errorDetail'])))
        if 0 <= res.status_code - 500 <= 12:
            raise FourSquareApiException(decoded_response['meta']['errorDetail'])

        return decoded_response


class ReservationsConsumer:

    def __init__(self, endpoint_url,):
        self.endpoint_url = endpoint_url


    def get_recent_reservations(self):
        return []

    
class ReservationsUpdater:
    def update_reservations(self, reservations):
        pass