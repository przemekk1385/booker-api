from datetime import date, timedelta

from django.apps import apps
from django.db.models import ExpressionWrapper, F, Q, fields
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from booker_api.models import Booking, Stay

DAYS_BETWEEN_BOOKINGS = apps.get_app_config("booker_api").days_between_bookings


class BookingSerializer(serializers.ModelSerializer):
    apartment = serializers.SerializerMethodField(read_only=True)
    slot_label = serializers.SerializerMethodField(read_only=True)

    identifier = serializers.CharField(write_only=True)

    class Meta:
        fields = ("apartment", "day", "identifier", "slot", "slot_label")
        model = Booking

    def create(self, validated_data):
        return Booking.objects.create(
            stay=validated_data["stay"],
            day=validated_data["day"],
            slot=validated_data["slot"],
        )

    def get_apartment(self, obj):
        return obj.stay.apartment.label

    def get_slot_label(self, obj):
        return obj.get_slot_display()

    def validate(self, attrs):
        identifier = attrs.pop("identifier")
        day = attrs["day"]

        try:
            stay = Stay.objects.filter(date_from__lte=day, date_to__gte=day).get(
                identifier=identifier
            )
        except Stay.DoesNotExist as e_info:
            raise serializers.ValidationError(
                {
                    "identifier": _(
                        f"There is no stay associated with identifier {identifier}."
                    )
                }
            ) from e_info

        blocked_days = [
            day + timedelta(days=i)
            for i in range(-DAYS_BETWEEN_BOOKINGS + 1, DAYS_BETWEEN_BOOKINGS)
        ]
        if Booking.objects.filter(
            day__in=blocked_days,
            stay=stay,
        ).exists():
            msg = (
                _("Booking is possible once per day.")
                if DAYS_BETWEEN_BOOKINGS == 1
                else _(f"Booking is possible once per {DAYS_BETWEEN_BOOKINGS} days.")
            )
            raise serializers.ValidationError({"day": msg})

        attrs["stay"] = stay
        return attrs

    def validate_day(self, val):
        if val < date.today():
            raise serializers.ValidationError(_(f"{val} already passed."))

        return val


class SlotSerializer(serializers.BaseSerializer):
    def create(self, validated_data):
        raise NotImplementedError("SlotSerializer is read-only.")

    def update(self, instance, validated_data):
        raise NotImplementedError("SlotSerializer is read-only.")

    def to_internal_value(self, data):
        raise NotImplementedError("SlotSerializer is read-only.")

    def to_representation(self, instance):
        return {
            "label": instance.label,
            "name": instance.name,
            "value": instance.value,
        }
