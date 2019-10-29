from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient

from rest import views


class RolesViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_list_roles(self):
        request = self.factory.get('/recommendations')
        view = views.RecommendationsView()
        res = view.dispatch(request)
        self.assertEqual(200, res.status_code)
        self.assertIn('results', res.data)
        for k, v in res.data['results'].items():
            self.assertGreater(len(v), 0)
