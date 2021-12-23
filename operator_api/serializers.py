from rest_framework import serializers

from booker_api.models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    id = serializers.IntegerField(read_only=True)
    number = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Apartment
