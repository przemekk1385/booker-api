from rest_access_policy import AccessPolicy
from rest_framework import mixins, viewsets

from booker_api.models import Apartment
from operator_api.serializers import ApartmentSerializer


class ApartmentAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["retrieve", "update", "partial_update"],
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
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Apartment.objects.all()
    permission_classes = (ApartmentAccessPolicy,)
    serializer_class = ApartmentSerializer
