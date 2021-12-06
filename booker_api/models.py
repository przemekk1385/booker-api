from django.db import models
from django.utils.translation import gettext_lazy as _


class Stay(models.Model):
    class Apartment(models.IntegerChoices):
        APARTMENT_1 = 1, _("APARTMENT 1")
        APARTMENT_2 = 2, _("APARTMENT 2")

    apartment = models.PositiveSmallIntegerField(
        choices=Apartment.choices,
    )
    identifier = models.CharField(max_length=9)
    date_from = models.DateField()
    date_to = models.DateField()


class Booking(models.Model):
    class Slot(models.IntegerChoices):
        FROM11 = 1, "11:00 - 11:50"
        FROM12 = 2, "12:00 - 12:50"
        FROM13 = 3, "13:00 - 13:50"
        FROM14 = 4, "14:00 - 14:50"

    class Meta:
        unique_together = ("day", "slot")

    stay = models.ForeignKey(Stay, on_delete=models.CASCADE)

    day = models.DateField()
    slot = models.PositiveSmallIntegerField(choices=Slot.choices)