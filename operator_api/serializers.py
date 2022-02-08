from rest_framework import serializers

from booker_api.models import Apartment, Booking


class ApartmentSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    id = serializers.IntegerField(read_only=True)
    number = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Apartment


class BookingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ("id", "apartment", "day", "slot")
        model = Booking
