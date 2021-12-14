from datetime import date, timedelta

from rest_framework import mixins, viewsets

from booker_api.models import Booking
from booker_api.serializers import BookingSerializer


class BookingViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(
            day__in=[date.today(), date.today() + timedelta(days=1)]
        )
