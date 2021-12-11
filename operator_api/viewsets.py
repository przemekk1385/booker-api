from rest_framework import viewsets

from booker_api.models import Stay
from operator_api.serializers import StaySerializer


class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer
