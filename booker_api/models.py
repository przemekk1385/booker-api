from django.contrib.auth.models import AbstractUser
from django.db import models


class Apartment(models.Model):
    label = models.CharField(max_length=20)


class Stay(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=9)
    date_from = models.DateField()
    date_to = models.DateField()

    class Meta:
        unique_together = ("apartment", "date_from", "date_to")


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


class User(AbstractUser):
    apartments = models.ManyToManyField(Apartment, related_name="apartments")
