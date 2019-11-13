import collections

from sync.exceptions import EmptyCityNameException


class VenueRepositoryRaisesExceptionMock:
    def get_venues(self, near, intent, query):
        raise EmptyCityNameException('some shit')


class VenueRepositoryNotEmptyMock:
    def get_venues(self, near, intent, query):
        return {'response':{'venues':[34,345,46,76]}}


class VenueRepositoryEmptyMock:
    def get_venues(self, near, intent, query):
        return {'response':{'venues':[]}}


class ReservationsRetrieveEmptyMock:
    def retrieve_recent_reservations(self):
        return []


Reservation = collections.namedtuple('Reservation', 'date destination reservation_id')


class ReservationsRetrieveNonEmptyMock:
    def retrieve_recent_reservations(self):
        return [Reservation(reservation_id="sdfjsdjfsd", date='2020-01-13T12:52:58.432488', destination='Mumbai, India')]