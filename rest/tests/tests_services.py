from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient

from rest import views


class RecommendationsServiceTest(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()
