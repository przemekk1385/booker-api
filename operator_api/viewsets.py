from rest_access_policy import AccessPolicy
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from booker_api.models import Apartment
from booker_api.utils import make_code
from operator_api.serializers import ApartmentSerializer


class ApartmentAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["retrieve", "update", "partial_update", "refresh_code"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": "is_operator",
        },
    ]

    @staticmethod
    def is_operator(request, view, view_action: str) -> bool:
        return request.user.apartments.filter(pk=view.kwargs.get("pk")).exists()


class ApartmentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Apartment.objects.all()
    permission_classes = (ApartmentAccessPolicy,)
    serializer_class = ApartmentSerializer

    @action(detail=True, url_path="refresh-code", methods=["POST"])
    def refresh_code(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.code = make_code()
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
