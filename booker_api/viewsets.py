from datetime import timedelta

from django.utils.datetime_safe import date
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings

from booker_api.models import Booking
from booker_api.serializers import BookingSerializer
from booker_api.utils import get_now


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

        now = get_now()
        deadline = (
            now.replace(
                year=instance.day.year,
                month=instance.day.month,
                day=instance.day.day,
                hour=instance.slot - 1,
                minute=30,
                second=0,
                microsecond=0,
            )
            - timedelta(microseconds=1)
        )
        if now > deadline:
            raise ValidationError(
                {
                    api_settings.NON_FIELD_ERRORS_KEY: _(
                        "Booking can be canceled up to 30 minutes before."
                    )
                }
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
