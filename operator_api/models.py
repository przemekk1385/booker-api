from django.contrib.auth.models import AbstractUser
from django.db import models

from booker_api.models import Apartment


class User(AbstractUser):
    apartments = models.ManyToManyField(Apartment, related_name="apartments")
