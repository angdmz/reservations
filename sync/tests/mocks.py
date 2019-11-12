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