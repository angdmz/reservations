from django.conf import settings
from django.test import TestCase

# Create your tests here.

from sync.services import HotelSearcher, generate_hotel_searcher, EmptyCityNameException, FourSquareApiConsumer

class VenueRepositoryRaisesExceptionMock:
    def get_venues(self, near, intent, query):
        raise EmptyCityNameException('some shit')

class VenueRepositoryNotEmptyMock:
    def get_venues(self, near, intent, query):
        return {'response':{'venues':[34,345,46,76]}}

class VenueRepositoryEmptyMock:
    def get_venues(self, near, intent, query):
        return {'response':{'venues':[]}}


class HotelSearcherTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_generate_searcher(self):
        searcher = generate_hotel_searcher()
        self.assertIsNotNone(searcher)

    def test_list_hotels(self):
        searcher = HotelSearcher(VenueRepositoryNotEmptyMock())
        hotels_near_capital = searcher.search_hotels_by_city('Capital Federal')
        self.assertIsNotNone(hotels_near_capital)
        self.assertNotEqual([], hotels_near_capital)

    def test_list_hotels_empty(self):
        searcher = HotelSearcher(VenueRepositoryRaisesExceptionMock())
        self.assertRaises(EmptyCityNameException, searcher.search_hotels_by_city, city_name='')

    def test_list_hotels_no_result(self):
        searcher = HotelSearcher(VenueRepositoryEmptyMock())
        no_hotels = searcher.search_hotels_by_city("Non existent city")
        self.assertEqual([], no_hotels)


class FourSquareApiConsumerIntegrationTest(TestCase):
    def setUp(self):
        pass

    def test_consume(self):
        consumer = FourSquareApiConsumer(settings.FOURSQUARE_API_ENDPOINT,
                                         settings.FOURSQUARE_API_CLIENT_ID,
                                         settings.FOURSQUARE_API_CLIENT_SECRET,
                                         settings.FOURSQUARE_API_VERSION)
        result = consumer.get_venues("buenos aires", "browse", "hotels")
        self.assertNotEqual([], result)
        self.assertIsNotNone(result)


class HotelSearcherIntegrationTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_generate_searcher(self):
        searcher = generate_hotel_searcher()
        self.assertIsNotNone(searcher)

    def test_list_hotels(self):
        searcher = generate_hotel_searcher()
        hotels_near_capital = searcher.search_hotels_by_city('Capital Federal')
        self.assertIsNotNone(hotels_near_capital)
        self.assertNotEqual([], hotels_near_capital)

    def test_list_hotels_empty(self):
        searcher = generate_hotel_searcher()
        self.assertRaises(EmptyCityNameException, searcher.search_hotels_by_city, city_name='')

    def test_list_hotels_no_result(self):
        searcher = generate_hotel_searcher()
        no_hotels = searcher.search_hotels_by_city("Non existent city")
        self.assertEqual([], no_hotels)
