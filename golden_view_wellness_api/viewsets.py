from rest_framework import mixins, viewsets

from golden_view_wellness_api.models import Booking
from golden_view_wellness_api.serializers import BookingSerializer


class BookingViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
