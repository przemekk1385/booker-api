from rest_framework import routers

from booker_api import viewsets

router = routers.DefaultRouter()
router.register("booking", viewsets.BookingViewSet, basename="booking")
