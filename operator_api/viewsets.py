from rest_access_policy import AccessPolicy
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from booker_api.models import Stay
from operator_api.serializers import StaySerializer


class StayAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "*",
            "effect": "allow",
        },
        {
            "action": ["create"],
            "principal": "*",
            "effect": "allow",
            "condition": "can_create",
        },
        {
            "action": ["update", "partial_update", "destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": "can_update_or_destroy",
        },
    ]

    @staticmethod
    def can_create(request, view, view_action: str) -> bool:
        return request.user.apartments.filter(id=request.data.get("apartment")).exists()

    @staticmethod
    def can_update_or_destroy(request, view, view_action: str) -> bool:
        return request.user.apartments.filter(
            id=view.get_object().apartment.id
        ).exists()


class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    permission_classes = (IsAuthenticated, StayAccessPolicy)
    serializer_class = StaySerializer
