from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class RecommendationsView(APIView):
    def dispatch(self, request, **kwargs):
        pass