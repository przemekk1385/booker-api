from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from booker_api.models import Booking, Stay, User

admin.site.register(Booking)
admin.site.register(Stay)
admin.site.register(User, UserAdmin)
