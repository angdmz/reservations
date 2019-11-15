import collections

from sync.tests.mocks import Reservation


class RecommendationsNotEmptyMock:

    def search_recommendations_for_destination(self, destination):
        Hotel = collections.namedtuple('Hotel', 'name place')
        response_dict = {
            'reservations':[
                Reservation(date='2019-10-10T10:10:10', destination="buenos aires", reservation_id="25345345345345"),
                Reservation(date='2019-12-10T16:10:10', destination="buenos aires", reservation_id="2dfdjfjd345345")
            ],
            'hotels': [
                Hotel(name="sarlanga", place="poronga")
            ]
        }
        return response_dict