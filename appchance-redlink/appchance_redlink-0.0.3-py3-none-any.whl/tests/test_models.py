# pylint: disable=protected-access
from unittest.mock import MagicMock, call

from django.conf import settings

import pytest
from redlink import app_settings
from redlink.models import RedlinkDevice
from redlink.redlink_client import ActionType, ReceiverType
from redlink.tests.factories import RedlinkDeviceFactory


@pytest.mark.django_db
class TestRedlinkDeviceQuerySet:
    def setup(self):
        app_settings.REDLINK_DEFAULT_LANGUAGE = "en"

    def test_send_push__single_device(self):
        device = RedlinkDeviceFactory()
        queryset = RedlinkDevice.objects.get_queryset()
        queryset._redlink_client = MagicMock()
        queryset.send_push(
            title="Test push",
            body="Test body",
            external_data={"test1": "test data 1", "test2": "test data 2"},
        )
        queryset._redlink_client.send_push.assert_called_with(
            applications=[settings.REDLINK_ANDROID_APP_ID, settings.REDLINK_IOS_APP_ID],
            to=[
                {
                    "receiver": device.registration_id,
                    "type": ReceiverType.DEVICE_RECEIVER,
                }
            ],
            title={"en": "Test push"},
            body={"en": "Test body"},
            external_data={"test1": "test data 1", "test2": "test data 2"},
            action_type=ActionType.WEBVIEW.value,
            default_language="en",
        )

    def test_send_push__multiple_devices__chunk(self):
        device = sorted(RedlinkDeviceFactory.create_batch(3), key=lambda obj: obj.id)
        queryset = RedlinkDevice.objects.get_queryset()
        queryset._redlink_client = MagicMock()
        queryset.CHUNK_SIZE = 2
        queryset.send_push(
            title="Test push",
            body="Test body",
            external_data={"test1": "test data 1", "test2": "test data 2"},
        )
        queryset._redlink_client.send_push.assert_has_calls(
            calls=[
                call(
                    applications=[
                        settings.REDLINK_ANDROID_APP_ID,
                        settings.REDLINK_IOS_APP_ID,
                    ],
                    to=[
                        {
                            "receiver": device[0].registration_id,
                            "type": ReceiverType.DEVICE_RECEIVER,
                        },
                        {
                            "receiver": device[1].registration_id,
                            "type": ReceiverType.DEVICE_RECEIVER,
                        },
                    ],
                    title={"en": "Test push"},
                    body={"en": "Test body"},
                    external_data={"test1": "test data 1", "test2": "test data 2"},
                    action_type=ActionType.WEBVIEW.value,
                    default_language="en",
                ),
                call(
                    applications=[
                        settings.REDLINK_ANDROID_APP_ID,
                        settings.REDLINK_IOS_APP_ID,
                    ],
                    to=[
                        {
                            "receiver": device[2].registration_id,
                            "type": ReceiverType.DEVICE_RECEIVER,
                        }
                    ],
                    title={"en": "Test push"},
                    body={"en": "Test body"},
                    external_data={"test1": "test data 1", "test2": "test data 2"},
                    action_type=ActionType.WEBVIEW.value,
                    default_language="en",
                ),
            ]
        )


@pytest.mark.django_db
class TestRedlinkDevice:
    def test_send_push(self):
        device: RedlinkDevice = RedlinkDeviceFactory()
        device._redlink_client = MagicMock(DEFAULT_LANGUAGE="en")

        device.send_push(
            title="Test push",
            body="Test body",
            external_data={"test1": "test data 1", "test2": "test data 2"},
        )
        device._redlink_client.send_push.assert_called_with(  # type: ignore
            applications=[settings.REDLINK_ANDROID_APP_ID, settings.REDLINK_IOS_APP_ID],
            to=[
                {
                    "receiver": device.registration_id,
                    "type": ReceiverType.DEVICE_RECEIVER,
                }
            ],
            title={"en": "Test push"},
            body={"en": "Test body"},
            external_data={"test1": "test data 1", "test2": "test data 2"},
            action_type=ActionType.WEBVIEW.value,
            default_language="en",
        )
