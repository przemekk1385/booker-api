from django.contrib import admin

from booker_api.models import Apartment, Booking

admin.site.register(Booking)


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    fields = ["code", "number"]
    readonly_fields = ["number"]
