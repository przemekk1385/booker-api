from django.contrib import admin

from booker_api.models import Apartment, Booking, Stay

admin.site.register(Apartment)
admin.site.register(Booking)
admin.site.register(Stay)
