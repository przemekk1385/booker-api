from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from booker_api.models import Apartment
from operator_api.serializers import ApartmentSerializer


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def apartment_list(request):
    queryset = Apartment.objects.all()
    serializer = ApartmentSerializer(queryset, many=True)

    return Response(data=serializer.data)
