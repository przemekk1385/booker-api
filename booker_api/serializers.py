from datetime import timedelta

from django.apps import apps
from django.utils.datetime_safe import date
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.settings import api_settings

from booker_api.models import Apartment, Booking
from booker_api.utils import get_now


class BookingSerializer(serializers.ModelSerializer):
    apartment = serializers.SlugRelatedField("number", read_only=True)

    code = serializers.CharField(write_only=True)

    class Meta:
        fields = ("apartment", "code", "day", "slot")
        model = Booking

    def create(self, validated_data):
        apartment = get_object_or_404(Apartment, code=validated_data["code"])

        return Booking.objects.create(
            apartment=apartment,
            day=validated_data["day"],
            slot=validated_data["slot"],
        )

    @staticmethod
    def get_slot_label(obj):
        return obj.get_slot_display()

    def validate(self, attrs):
        days_between_bookings = apps.get_app_config("booker_api").days_between_bookings

        code, day, slot = attrs["code"], attrs["day"], attrs["slot"]

        now = get_now()

        if day == now.date() and now.hour in [20, 21]:
            raise serializers.ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: _("Cannot book after 8 p.m.")}
            )

        apartment = get_object_or_404(Apartment, code=code)

        blocked_days = [
            day + timedelta(days=i)
            for i in range(-days_between_bookings + 1, days_between_bookings)
        ]
        if Booking.objects.filter(
            day__in=blocked_days,
            apartment=apartment,
        ).exists():
            msg = (
                _("Booking is possible once per day.")
                if days_between_bookings == 1
                else _("Booking is possible once per %(days)s days.")
                % {"days": days_between_bookings}
            )

            raise serializers.ValidationError({"day": msg})

        if day == now.date() and slot <= now.hour:
            raise serializers.ValidationError(
                {"slot": _("%(hour)s o'clock has already passed.") % {"hour": slot}}
            )

        return attrs

    def validate_day(self, val):
        if val < date.today():
            raise serializers.ValidationError(
                _("%(day)s already passed.") % {"day": val}
            )

        return val


class SlotSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "name": instance.name,
            "value": instance.value,
        }
