from datetime import date, timedelta

from rest_framework import serializers, status, views
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from booker_api.models import Booking
from booker_api.serializers import BookingSerializer, SlotSerializer


class BookingDeleteRequest(serializers.Serializer):
    code = serializers.CharField()
    day = serializers.DateField()


class BookingView(views.APIView):
    serializer_class = BookingSerializer

    def get_object(self, code: str, day: date) -> Booking:
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, apartment__code=code, day=day)
        return obj

    def get_queryset(self):
        return Booking.objects.filter(day__gte=date.today() - timedelta(days=1))

    def get(self, request: Request) -> Response:
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request: Request) -> Response:
        delete_request = BookingDeleteRequest(data=request.data)
        delete_request.is_valid(raise_exception=True)

        instance = self.get_object(**delete_request.data)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(("GET",))
def health_status(request: Request) -> Response:
    return Response({}, status=status.HTTP_200_OK)


@api_view(["GET"])
def slot_list(request: Request) -> Response:
    serializer = SlotSerializer(Booking.Slot, many=True)

    return Response(data=serializer.data)
