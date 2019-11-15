import coreapi

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest.schemas import CustomSchema
from rest.services import generate_recommendation_service


class RecommendationsView(APIView):
    """ Servicio de recomendaciones """

    schema = CustomSchema(fields_get=[
        coreapi.Field('destination',
                      required=True,
                      description="Destination to look for recommendations", ),
    ], )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recommendation_service = kwargs.get('recommendation_service', generate_recommendation_service())

    def get(self, request):
        """
        Lists reservations and hotels for given destination
        """
        if not 'destination' in request.query_params:
            return Response({'message':"Destination parameter not set"}, status=status.HTTP_412_PRECONDITION_FAILED)
        destination = request.query_params.get('destination')
        recommendations = self.recommendation_service.search_recommendations_for_destination(destination)
        return Response({'results': recommendations}, status=status.HTTP_200_OK)