from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class Apartment(models.Model):
    label = models.CharField(max_length=20)

    def __repr__(self):
        return f"<{self.__class__.__name__} label={self.label}>"

    def __str__(self):
        return self.label


class Stay(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=9)
    date_from = models.DateField()
    date_to = models.DateField()

    class Meta:
        unique_together = ("apartment", "date_from", "date_to")

    @property
    def formatted_identifier(self):
        return "-".join([self.identifier[i : i + 3] for i in range(0, 9, 3)])

    def __repr__(self):
        return f"<{self.__class__.__name__} apartment={self.apartment} identifier={self.identifier}>"

    def __str__(self):
        return f"{self.apartment} {self.formatted_identifier}"


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

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f" day={self.day}"
            f" slot={self.get_slot_display()}"
            f" identifier={self.stay.identifier}>"
        )

    def __str__(self):
        return f"{self.day} {self.get_slot_display()} {self.stay.formatted_identifier}"
