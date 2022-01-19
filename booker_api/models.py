from django.db import models
from django.utils.translation import gettext as _


class Apartment(models.Model):
    class Meta:
        verbose_name = _("apartment")
        verbose_name_plural = _("apartments")

    code = models.CharField(max_length=10, unique=True, verbose_name=_("code"))
    number = models.PositiveSmallIntegerField(verbose_name=_("number"))

    def __repr__(self):
        return f"<{self.__class__.__name__} code={self.code} number={self.number}>"

    def __str__(self):
        return _(f"Apartment {self.number}")

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.pk + 1
        super(Apartment, self).save(*args, **kwargs)


class Booking(models.Model):
    class Slot(models.IntegerChoices):
        FROM11 = 11, "11:00 - 11:50"
        FROM12 = 12, "12:00 - 12:50"
        FROM13 = 13, "13:00 - 13:50"
        FROM14 = 14, "14:00 - 14:50"
        FROM15 = 15, "15:00 - 15:50"
        FROM16 = 16, "16:00 - 16:50"
        FROM17 = 17, "17:00 - 17:50"
        FROM18 = 18, "18:00 - 18:50"
        FROM19 = 19, "19:00 - 19:50"
        FROM20 = 20, "20:00 - 20:50"
        FROM21 = 21, "21:00 - 21:50"

    class Meta:
        unique_together = ("day", "slot")
        verbose_name = _("booking")
        verbose_name_plural = _("bookings")
        ordering = ("-day", "slot")

    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, verbose_name=_("apartment")
    )

    day = models.DateField(verbose_name=_("day"))
    slot = models.PositiveSmallIntegerField(
        choices=Slot.choices, verbose_name=_("slot")
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f" day={self.day}"
            f" slot={self.get_slot_display()}"
            f" apartment={self.apartment.number}>"
        )

    def __str__(self):
        return _(
            f"{self.day} {self.get_slot_display()} Apartment {self.apartment.number}"
        )
