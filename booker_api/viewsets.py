from datetime import timedelta

from django.utils.datetime_safe import date
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from booker_api.models import Booking
from booker_api.serializers import BookingSerializer


class BookingCancelRequest(serializers.Serializer):
    code = serializers.CharField()
    day = serializers.DateField()


class BookingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_object(self):
        return (
            get_object_or_404(
                self.get_queryset(),
                apartment__code=self.request.data["code"],
                day=self.request.data["day"],
            )
            if self.action == "cancel"
            else super().get_object()
        )

    def get_queryset(self):
        return Booking.objects.filter(day__gte=date.today() - timedelta(days=1))

    @action(detail=False, url_path="cancel", methods=["POST"])
    def cancel(self, request, *args, **kwargs):
        cancel_request = BookingCancelRequest(data=request.data)
        cancel_request.is_valid(raise_exception=True)

        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
