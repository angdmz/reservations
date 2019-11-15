import time

from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient

from rest import views
from rest.tests.mocks import RecommendationsNotEmptyMock
from sync.services import generate_reservations_updater
from zones.models import Country


class RecommendationssViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_list_reservations_valid_destination(self):
        request = self.factory.get('/recommendations/?destination=buenos%20aires')
        view = views.RecommendationsView()
        view.some_mock = RecommendationsNotEmptyMock()
        res = view.dispatch(request)
        self.assertEqual(200, res.status_code)
        self.assertIn('results', res.data)
        self.assertIn('reservations', res.data.get('results'))
        self.assertIn('hotels', res.data.get('results'))
        for reserva in res.data['results']['reservations']:
            self.assertIn('reservation_id', reserva)
            self.assertIn('date', reserva)
            self.assertIn('destination', reserva)
            self.assertEqual(reserva['destination'], "buenos aires")

        for hotel in res.data['results']['hotels']:
            self.assertIn('name', hotel)
            self.assertIn('address', hotel)
            self.assertIn('place', hotel)
            self.assertEqual('place', 'buenos aires')

    def test_no_destination(self):
        request = self.factory.get('/recommendations/')
        view = views.RecommendationsView()
        res = view.dispatch(request)
        self.assertEqual(412, res.status_code)
        self.assertIn('message', res.data)
        self.assertEqual('Destination parameter not set', res.data['message'])

class RecommendationsViewIntegrationTest(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.countries_manager = Country.objects
        self.updater = generate_reservations_updater()

    def test_list_reservations_valid_destination(self):
        request = self.factory.get('/recommendations/?destination=Buenos%20Aires,%20Argentina')
        view = views.RecommendationsView()

        while not self.countries_manager.exists_place("Buenos Aires, Argentina"):
            self.updater.update_reservations()
            time.sleep(1)

        res = view.dispatch(request)
        self.assertEqual(200, res.status_code)
        self.assertIn('results', res.data)
        self.assertIn('reservations', res.data.get('results'))
        self.assertIn('hotels', res.data.get('results'))
        for reserva in res.data['results']['reservations']:
            self.assertIn('reservation_id', reserva)
            self.assertIn('date', reserva)
            self.assertIn('destination', reserva)
            self.assertEqual(reserva['destination'], "Buenos Aires, Argentina")

        for hotel in res.data['results']['hotels']:
            self.assertIn('name', hotel)
            self.assertIn('address', hotel)
            self.assertIn('place', hotel)
            self.assertEqual('place', 'Buenos Aires, Argentina')

    def test_no_destination(self):
        request = self.factory.get('/recommendations/')
        view = views.RecommendationsView()
        res = view.dispatch(request)
        self.assertEqual(412, res.status_code)
        self.assertIn('message', res.data)
        self.assertEqual('Destination parameter not set', res.data['message'])