from django.conf import settings
from django.utils import timezone

import pytest
from freezegun import freeze_time
from redlink.models import RedlinkDevice
from redlink.serializers import RedlinkDeviceSerializer
from redlink.tests.factories import RedlinkDeviceFactory


@pytest.mark.django_db
class TestRedlinkDeviceSerializer:
    @freeze_time()
    def test_serialize(self):
        device: RedlinkDevice = RedlinkDeviceFactory()
        serializer = RedlinkDeviceSerializer(device)

        now = timezone.localtime(timezone.now()).strftime(settings.DATETIME_FORMAT)
        assert serializer.data == {
            "id": str(device.id),
            "registration_id": device.registration_id,
            "user": device.user_id,
            "name": device.name,
            "active": device.active,
            "type": device.type,
            "created": now,
            "updated": now,
        }
