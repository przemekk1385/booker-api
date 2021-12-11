from rest_framework import serializers

from booker_api.models import Stay


class StaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Stay
