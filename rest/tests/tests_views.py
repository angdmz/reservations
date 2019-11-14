from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient

from rest import views


class RecommendationssViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_list_reservations_valid_destination(self):
        request = self.factory.get('/recommendations/?destination=buenos%20aires')
        view = views.RecommendationsView()
        view.some_mock = None
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
