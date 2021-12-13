from rest_framework.decorators import api_view
from rest_framework.response import Response

from booker_api.models import Booking
from booker_api.serializers import SlotSerializer


@api_view(["GET"])
def slot_list(request):
    serializer = SlotSerializer(Booking.Slot, many=True)

    return Response(data=serializer.data)
