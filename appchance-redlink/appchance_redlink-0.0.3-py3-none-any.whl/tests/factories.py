import factory
from factory import Faker
from redlink.models import RedlinkDevice, SentPush


class RedlinkDeviceFactory(factory.django.DjangoModelFactory):
    name = Faker("pystr", max_chars=10)
    registration_id = Faker("pystr", max_chars=10)
    type = factory.Iterator(["android", "ios"])

    class Meta:
        model = RedlinkDevice


class SentPushFactory(factory.django.DjangoModelFactory):
    content = Faker("pyint")

    class Meta:
        model = SentPush
