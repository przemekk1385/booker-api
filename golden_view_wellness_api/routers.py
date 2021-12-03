from rest_framework import routers

from golden_view_wellness_api import viewsets

router = routers.DefaultRouter()
router.register("booking", viewsets.BookingViewSet, basename="booking")
