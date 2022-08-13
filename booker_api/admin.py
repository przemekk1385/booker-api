from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

from booker_api.models import Apartment, Booking
from booker_api.utils import get_now


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    fields = ["code", "number"]
    readonly_fields = ["number"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request: WSGIRequest, obj: Booking = None):
        now = get_now()

        return (
            True
            if not obj
            else any(
                [obj.day == now.date() and obj.slot > now.hour, obj.day > now.date()]
            )
        )
