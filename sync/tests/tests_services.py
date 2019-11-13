from django.conf import settings
from django.test import TestCase

# Create your tests here.
from reservations.models import Reservation
from sync.services import HotelSearcher, generate_hotel_searcher, FourSquareApiConsumer, generate_reservations_retriever, ReservationsUpdater, generate_reservations_updater
from sync.exceptions import EmptyCityNameException
from sync.tests.mocks import VenueRepositoryRaisesExceptionMock, VenueRepositoryNotEmptyMock, VenueRepositoryEmptyMock, \
    ReservationsRetrieveEmptyMock, ReservationsRetrieveNonEmptyMock


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


class ReservationsRetrieverTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_retrieve_reservations(self):
        retriever = generate_reservations_retriever()
        reservations = retriever.retrieve_recent_reservations()
        self.assertIsNotNone(reservations)

    def test_retrieve_empty_reservations(self):
        retriever = generate_reservations_retriever()
        reservations = retriever.retrieve_recent_reservations()
        self.assertEqual([], reservations)

    def test_generate_new_retriever(self):
        retriever = generate_reservations_retriever()
        self.assertIsNotNone(retriever)


class ReservationsUpdaterTest(TestCase):

    def setUp(self):
        self.reservations_manager = Reservation.objects

    def test_generate_reservations_updater(self):
        updater = generate_reservations_updater()
        self.assertIsNotNone(updater)

    def test_update_reservations(self):
        updater = ReservationsUpdater(ReservationsRetrieveNonEmptyMock())
        updated, new_reservations =  updater.update_reservations()
        self.assertTrue(updated)
        self.assertNotEqual({}, new_reservations)
        for new in new_reservations:
            self.assertTrue(self.reservations_manager.exists_reservation_with_id(new.reservation_id))

    def test_update_no_reservations(self):
        updater = ReservationsUpdater(ReservationsRetrieveEmptyMock())
        updated, new_reservations = updater.update_reservations()
        self.assertFalse(updated)
        self.assertEqual({}, new_reservations)


class ReservationsUpdaterIntegrationTest(TestCase):

    def test_(self):
        pass
