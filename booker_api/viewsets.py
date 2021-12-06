from rest_framework import mixins, viewsets

from booker_api.models import Booking
from booker_api.serializers import BookingSerializer


class BookingViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
