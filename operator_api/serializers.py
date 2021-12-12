from rest_framework import serializers

from booker_api.models import Apartment, Stay


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Apartment


class StaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Stay
