from rest_framework import routers

from operator_api import viewsets

router = routers.DefaultRouter()
router.register("apartment", viewsets.ApartmentViewSet, basename="apartment")
