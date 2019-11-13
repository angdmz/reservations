from django.contrib import admin

# Register your models here.
from hotels.models import Hotel
from reservations.models import Reservation
from zones.models import Country as Destination

admin.site.register(Hotel)
admin.site.register(Destination)
admin.site.register(Reservation)