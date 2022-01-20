from django.db import models
from django.utils.translation import gettext, gettext_lazy


class Apartment(models.Model):
    class Meta:
        verbose_name = gettext_lazy("apartment")
        verbose_name_plural = gettext_lazy("apartments")

    code = models.CharField(gettext_lazy("code"), max_length=10, unique=True)
    number = models.PositiveSmallIntegerField(gettext_lazy("number"))

    def __repr__(self):
        return f"<{self.__class__.__name__} code={self.code} number={self.number}>"

    def __str__(self):
        return gettext("Apartment %(number)s" % {"number": self.number})

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
        verbose_name = gettext_lazy("booking")
        verbose_name_plural = gettext_lazy("bookings")
        ordering = ("-day", "slot")

    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, verbose_name=gettext_lazy("apartment")
    )

    day = models.DateField(gettext_lazy("day"))
    slot = models.PositiveSmallIntegerField(gettext_lazy("slot"), choices=Slot.choices)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f" day={self.day}"
            f" slot={self.get_slot_display()}"
            f" apartment={self.apartment.number}>"
        )

    def __str__(self):
        return gettext("%(day)s %(slot)s Apartment %(number)s") % {
            "day": self.day,
            "slot": self.get_slot_display(),
            "number": self.apartment.number,
        }
