# pylint: disable=protected-access
from unittest.mock import ANY, MagicMock, patch

from django.conf import settings

import pytest
from redlink.errors import (
    RedlinkAuthorizationError,
    RedlinkNotFoundError,
    RedlinkServerError,
)
from redlink.redlink_client import ActionType, ReceiverType, RedlinkClient


class TestRedlinkClient:
    def test_parse__minimal_data(self,):
        redlink_client = RedlinkClient("test_api_key")
        payload = redlink_client._parse_payload(
            applications=["XXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"],
            title="Test title",
            body="Test body",
            to=[{"receiver": "test-device", "type": ReceiverType.DEVICE_RECEIVER}],
        )
        assert payload == {
            "applications": ["XXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"],
            "to": [
                {"receiver": "test-device", "type": ReceiverType.DEVICE_RECEIVER.value}
            ],
            "title": {"en": "Test title"},
            "body": {"en": "Test body"},
            "defaultLanguage": "en",
            "scheduleTime": ANY,
            "externalData": {},
            "action": {"type": ActionType.NONE.value, "url": ""},
        }

    def test_parse__full_data(self):
        redlink_client = RedlinkClient("test_api_key")
        payload = redlink_client._parse_payload(
            applications=["XXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"],
            title={"pl": "Test title"},
            body={"pl": "Test body"},
            to=[
                {
                    "receiver": "example-device-id",
                    "type": ReceiverType.DEVICE_RECEIVER,
                    "external_id": "ext_id_1",
                },
                {
                    "receiver": "+48123123123",
                    "type": ReceiverType.NUMBER_RECEIVER,
                    "external_id": "ext_id_2",
                },
                {
                    "receiver": "exail@example.com",
                    "type": ReceiverType.EMAIL_RECEIVER,
                    "external_id": "ext_id_3",
                },
            ],
            default_language="pl",
            silent=False,
            sound="/relative-sound-file-path",
            image="http://absolute.url/to/image",
            schedule_time="2020-07-09 12:00:00",
            ttl=123412,
            external_data={"test": "x", "test1": False},
            subtitle="subtitle-only-ios",
            lockscreen_visibility=1,
            icon_small="/relative-icon-file-path",
            icon_large="/relative-icon-file-path",
            action_url="http://absolute.url/to/redirect/on/click",
            action_type=2,
            action_buttons=[
                {
                    "button": 1,
                    "icon": "icon-path",
                    "action": {"url": "string", "type": 0},
                }
            ],
        )

        assert payload == {
            "applications": ["XXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"],
            "to": [
                {
                    "receiver": "example-device-id",
                    "type": ReceiverType.DEVICE_RECEIVER.value,
                    "external_id": "ext_id_1",
                },
                {
                    "receiver": "+48123123123",
                    "type": ReceiverType.NUMBER_RECEIVER.value,
                    "external_id": "ext_id_2",
                },
                {
                    "receiver": "exail@example.com",
                    "type": ReceiverType.EMAIL_RECEIVER.value,
                    "external_id": "ext_id_3",
                },
            ],
            "title": {"pl": "Test title"},
            "body": {"pl": "Test body"},
            "defaultLanguage": "pl",
            "image": "http://absolute.url/to/image",
            "silent": False,
            "sound": "/relative-sound-file-path",
            "scheduleTime": "2020-07-09 12:00:00",
            "ttl": 123412,
            "externalData": {"test": "x", "test1": False},
            "advanced": {
                "subtitle": "subtitle-only-ios",
                "lockscreenVisibility": 1,
                "icon": {
                    "small": "/relative-icon-file-path",
                    "large": "/relative-icon-file-path",
                },
            },
            "action": {"url": "http://absolute.url/to/redirect/on/click", "type": 2},
            "actionButtons": [
                {
                    "button": 1,
                    "icon": "icon-path",
                    "action": {"url": "string", "type": 0},
                }
            ],
        }

    @patch("redlink.redlink_client.requests")
    def test_send_push(self, requests_mock):
        expected_response = MagicMock(status_code=200)
        requests_mock.post.return_value = expected_response
        redlink_client = RedlinkClient("test_api_key")
        response = redlink_client.send_push(
            applications=["XXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"],
            title="Test title",
            body="Test body",
            to=[{"receiver": "test-device", "type": ReceiverType.DEVICE_RECEIVER}],
        )
        assert response == expected_response

    @patch("redlink.redlink_client.requests")
    def test_send_push__anauthorized(self, requests_mock):
        requests_mock.post.return_value = MagicMock(status_code=401)
        redlink_client = RedlinkClient("test_api_key")
        with pytest.raises(RedlinkAuthorizationError):
            redlink_client.send_push(
                applications=["XXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"],
                title="Test title",
                body="Test body",
                to=[{"receiver": "test-device", "type": ReceiverType.DEVICE_RECEIVER}],
            )

    @patch("redlink.redlink_client.requests")
    def test_send_push__not_found(self, requests_mock):
        requests_mock.post.return_value = MagicMock(status_code=404)
        redlink_client = RedlinkClient("test_api_key")
        with pytest.raises(RedlinkNotFoundError):
            redlink_client.send_push(
                applications=["XXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"],
                title="Test title",
                body="Test body",
                to=[{"receiver": "test-device", "type": ReceiverType.DEVICE_RECEIVER}],
            )

    @patch("redlink.redlink_client.requests")
    def test_send_push__server_error(self, requests_mock):
        requests_mock.post.return_value = MagicMock(status_code=500)
        redlink_client = RedlinkClient(settings.REDLINK_API_KEY)
        with pytest.raises(RedlinkServerError):
            redlink_client.send_push(
                applications=["testapp"],
                title="Test title",
                body="Test body",
                to=[{"receiver": "test-device", "type": ReceiverType.DEVICE_RECEIVER}],
            )

    @pytest.mark.skip("Requires external redlink request.")
    def test_send_push__external(self):
        redlink_client = RedlinkClient(settings.REDLINK_API_KEY)
        response = redlink_client.send_push(
            applications=["e334cc4d-fc0d-4842-9b37-a6175d58a98f"],
            title="Test title",
            body="Test body",
            to=[
                {
                    "receiver": "cwwnofzRKWY:APA91bFnWFnFjG_kKUmNoNIRGt2SqHCGhVLp0hvz3fSQR-3xLuJFNe-TJ6R2ShFrUFjmaEwMWk"
                    "FQpWXXoE4vs-qXVG-HNAK_T1ac0RYhf7u1U3wBC20V2J5R8JKupmG24_1QUgSDYfZ4",
                    "type": ReceiverType.DEVICE_RECEIVER,
                }
            ],
        )
        assert response.status_code == 200
