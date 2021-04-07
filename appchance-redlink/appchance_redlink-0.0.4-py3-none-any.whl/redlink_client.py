# pylint: disable=too-many-arguments, too-many-locals, too-many-branches, no-else-raise
import json
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, TypedDict, Union

import requests
from redlink.errors import (
    RedlinkAuthorizationError,
    RedlinkNotFoundError,
    RedlinkServerError,
)


class ActionType(Enum):
    NONE = 1
    BROWSER = 2
    WEBVIEW = 3
    DEEPLINK = 4


class ReceiverType(Enum):
    DEVICE_RECEIVER = 1
    EMAIL_RECEIVER = 2
    NUMBER_RECEIVER = 3


class ReceiverDict(TypedDict, total=False):
    receiver: str
    external_id: Optional[str]
    type: ReceiverType


class RedlinkClient:
    def __init__(self, api_key):
        self.api_key = api_key

    DEFAULT_LANGUAGE = "en"
    URL = "https://api.redlink.pl/v1/push"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def send_push(
        self,
        applications: List[str],
        title: Union[str, Dict],
        body: Union[str, Dict],
        to: List[ReceiverDict],
        default_language: Optional[str] = None,
        silent: Optional[bool] = None,
        sound: Optional[str] = None,
        schedule_time: Optional[str] = None,
        ttl: Optional[int] = None,
        external_data: Optional[Dict] = None,
        subtitle: Optional[str] = None,
        lockscreen_visibility: Optional[int] = None,
        icon_small: Optional[str] = None,
        icon_large: Optional[str] = None,
        action_url: Optional[str] = None,
        action_type: Optional[int] = None,
        action_buttons: Optional[List[Dict]] = None,
    ):
        payload = self._parse_payload(
            applications=applications,
            to=to,
            title=title,
            body=body,
            default_language=default_language,
            silent=silent,
            sound=sound,
            schedule_time=schedule_time,
            ttl=ttl,
            subtitle=subtitle,
            lockscreen_visibility=lockscreen_visibility,
            external_data=external_data,
            icon_small=icon_small,
            icon_large=icon_large,
            action_url=action_url,
            action_type=action_type,
            action_buttons=action_buttons,
        )
        response = requests.post(
            url=self.URL, data=json.dumps(payload), headers=self.headers
        )
        return self._parse_response(response)

    @property
    def headers(self):
        return {"Authorization": self.api_key, "content-type": "application/json"}

    def _parse_payload(
        self,
        applications: List[str],
        title: Union[str, Dict],
        body: Union[str, Dict],
        to: List[ReceiverDict],
        default_language: Optional[str] = None,
        image: Optional[str] = None,
        silent: Optional[bool] = None,
        sound: Optional[str] = None,
        schedule_time: Optional[str] = None,
        ttl: Optional[int] = None,
        external_data: Optional[Dict] = None,
        subtitle: Optional[str] = None,
        lockscreen_visibility: Optional[int] = None,
        icon_small: Optional[str] = None,
        icon_large: Optional[str] = None,
        action_url: Optional[str] = None,
        action_type: Optional[int] = None,
        action_buttons: Optional[List[Dict]] = None,
    ):
        if default_language is None:
            default_language = self.DEFAULT_LANGUAGE

        if isinstance(title, str):
            title = {default_language: title}

        if isinstance(body, str):
            body = {default_language: body}

        payload: Dict = dict(
            applications=applications,
            to=dict(),
            title=title,
            body=body,
            defaultLanguage=default_language,
            scheduleTime=datetime.now().strftime(self.DATE_FORMAT),
            externalData=dict(),
            action=dict(type=ActionType.NONE.value, url=""),
        )

        for receiver in to:
            receiver["type"] = receiver["type"].value
        payload["to"] = to

        if image:
            payload["image"] = image
        if silent is not None:
            payload["silent"] = silent
        if sound:
            payload["sound"] = sound

        if schedule_time:
            payload["scheduleTime"] = schedule_time
        else:
            payload["scheduleTime"] = datetime.now().strftime(self.DATE_FORMAT)

        if ttl:
            payload["ttl"] = ttl
        if external_data:
            payload["externalData"] = external_data

        advanced: Dict = defaultdict(dict)
        if subtitle:
            advanced["subtitle"] = subtitle
        if lockscreen_visibility:
            advanced["lockscreenVisibility"] = lockscreen_visibility
        if icon_small:
            advanced["icon"]["small"] = icon_small
        if icon_large:
            advanced["icon"]["large"] = icon_large
        if advanced:
            payload["advanced"] = advanced
        if action_url:
            payload["action"].update({"url": action_url})
        if action_type:
            payload["action"].update({"type": action_type})

        if action_buttons:
            payload["actionButtons"] = action_buttons
        return payload

    def _parse_response(self, response):
        if response.status_code < 400:
            return response
        if response.status_code == 400:
            raise RedlinkAuthorizationError("Parse error.")
        if response.status_code == 401:
            raise RedlinkAuthorizationError("Invalid or missing token.")
        if response.status_code == 404:
            raise RedlinkNotFoundError("Receiver not found.")
        else:
            raise RedlinkServerError("Service unavailable.")
