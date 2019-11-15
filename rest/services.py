from hotels.models import Hotel
from reservations.models import Reservation


class RecommendationsService:

    hotel_manager = Hotel.objects
    reservation_manager = Reservation.objects

    def __init__(self):
        pass

    def search_recommendations_for_destination(self, destination):
        reservations = self.reservation_manager.find_reservations_by_destination(destination)
        reservations_list = [
            {'reservation_id': reservation.external_id,
             'date': reservation.date,
             'destination': reservation.destination.place}
            for reservation in reservations]
        hotels =  self.hotel_manager.find_hotels_by_place(destination)
        hotels_list = [{'name':hotel.name, 'address': hotel.address} for hotel in hotels ]
        return {'hotels':hotels_list, 'reservations': reservations_list}


def generate_recommendation_service():
    return RecommendationsService()
