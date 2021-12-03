from rest_framework import serializers

from golden_view_wellness_api.models import Booking, Stay


class BookingSerializer(serializers.ModelSerializer):
    apartment = serializers.SerializerMethodField(read_only=True)
    identifier = serializers.CharField(write_only=True)

    class Meta:
        fields = ("apartment", "day", "identifier", "slot")
        model = Booking

    def create(self, validated_data):
        return Booking.objects.create(
            stay=validated_data["stay"],
            day=validated_data["day"],
            slot=validated_data["slot"],
        )

    def get_apartment(self, obj):
        return obj.stay.get_apartment_display()

    def to_representation(self, instance):
        return {
            **super().to_representation(instance),
            "slot": instance.get_slot_display(),
        }

    def validate(self, attrs):
        identifier = attrs.pop("identifier")

        attrs["stay"] = Stay.objects.filter(
            date_from__lte=attrs["day"], date_to__gte=attrs["day"]
        ).get(identifier=identifier)

        return attrs
