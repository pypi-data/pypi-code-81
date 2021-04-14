from factory import Faker
from factory.django import DjangoModelFactory

from . import models


class HousingStatCredsFactory(DjangoModelFactory):
    owner = "admin"
    username = Faker("first_name")
    password = Faker("password")

    class Meta:
        model = models.HousingStatCreds
