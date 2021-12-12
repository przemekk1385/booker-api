from rest_access_policy import AccessPolicy
from rest_framework import viewsets

from booker_api.models import Stay
from operator_api.serializers import StaySerializer


class StayAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["create"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": "can_create",
        },
        {
            "action": ["update", "partial_update", "destroy"],
            "principal": "authenticated",
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
    permission_classes = (StayAccessPolicy,)
    serializer_class = StaySerializer
