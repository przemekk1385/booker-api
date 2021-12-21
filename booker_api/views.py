from datetime import date, timedelta

from django.utils.dateparse import parse_date
from rest_framework import status, views
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.fields import CharField, DateField, Field
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from booker_api.models import IDENTIFIER_MAX_LENGTH, Booking
from booker_api.serializers import BookingSerializer, SlotSerializer


class BookingView(views.APIView):
    serializer_class = BookingSerializer

    def _validate_delete_request_body(self):
        data = self.request.data

        errors = {
            field: [Field.default_error_messages["required"]]
            for field in ["day", "identifier"]
            if field not in data
        }

        if errors:
            raise ParseError(detail=errors)
        else:
            try:
                day = parse_date(data["day"])
            except (ValueError, TypeError):
                errors["day"] = DateField.default_error_messages["invalid"]
            else:
                if day is None:
                    errors["day"] = DateField.default_error_messages["invalid"]

            identifier = data["identifier"]
            if len(identifier) > IDENTIFIER_MAX_LENGTH:
                errors["identifier"] = CharField.default_error_messages["max_length"]

        if errors:
            raise ParseError(detail=errors)

        return day, identifier

    def get_object(self):
        day, identifier = self._validate_delete_request_body()

        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, day=str(day), stay__identifier=identifier)
        return obj

    def get_queryset(self):
        return Booking.objects.filter(day__gte=date.today() - timedelta(days=1))

    def get(self, _):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, _):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(("GET",))
def health_status(request):
    return Response({}, status=status.HTTP_200_OK)


@api_view(["GET"])
def slot_list(request):
    serializer = SlotSerializer(Booking.Slot, many=True)

    return Response(data=serializer.data)
