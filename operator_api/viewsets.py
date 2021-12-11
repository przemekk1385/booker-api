from rest_access_policy import AccessPolicy
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from booker_api.models import Stay
from operator_api.serializers import StaySerializer


class StayAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list"],
            "principal": "*",
            "effect": "allow",
        },
        {
            "action": ["create", "retrieve", "update", "partial_update", "destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_apartment_operator",
        },
    ]

    @staticmethod
    def is_apartment_operator(request, view, view_action: str) -> bool:
        print("foo")
        return True


class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    permission_classes = (IsAuthenticated, StayAccessPolicy)
    serializer_class = StaySerializer
