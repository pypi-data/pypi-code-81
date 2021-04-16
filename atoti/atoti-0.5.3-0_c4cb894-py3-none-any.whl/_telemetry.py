from __future__ import annotations

import json
import os
import platform
from abc import ABC
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from typing import Optional
from urllib.request import Request, urlopen
from uuid import UUID, uuid4

from ._path_utils import get_atoti_home
from ._plugins import is_plugin_active
from ._version import VERSION

# Env var to toggle whether or not we collect telemetry data.
DISABLE_TELEMETRY_ENV_VAR = "ATOTI_DISABLE_TELEMETRY"

# Path where the installation's unique ID is stored.
_INSTALLATION_ID_PATH = get_atoti_home() / "installation_id.txt"

_TELEMETRY_SERVICE_URL = "https://rob2s0lazk.execute-api.eu-west-3.amazonaws.com/events"

TELEMETRY_ASYNC_EXECUTOR = ThreadPoolExecutor(max_workers=1)


@dataclass(frozen=True)
class TelemetryEvent(ABC):

    event_type: str = field(init=False)

    def _set_event_type(self, event_type: str):
        # The dataclass is frozen, so we can't assign to this field directly
        object.__setattr__(self, "event_type", event_type)


@dataclass(frozen=True)
class ImportEvent(TelemetryEvent):
    """Triggered when the library is imported."""

    installation_id: str
    operating_system: str
    version: str

    def __post_init__(self):
        self._set_event_type("import")


def send_event_to_telemetry_service(event: TelemetryEvent):
    body = json.dumps(asdict(event)).encode("utf8")
    headers = {"Content-Type": "application/json"}
    request = Request(
        _TELEMETRY_SERVICE_URL,
        data=body,
        headers=headers,
        method="POST",
    )
    TELEMETRY_ASYNC_EXECUTOR.submit(urlopen, request)


def disabled_by_atoti_plus() -> bool:
    return is_plugin_active("plus")


def disabled_by_environment_variable() -> bool:
    return os.environ.get(DISABLE_TELEMETRY_ENV_VAR, "False").lower() == "true"


def get_installation_id_from_file() -> Optional[str]:
    if not _INSTALLATION_ID_PATH.exists():
        return None

    try:
        content = _INSTALLATION_ID_PATH.read_text(encoding="utf8").strip()
        UUID(content)
        return content
    except:  # nosec  pylint: disable=bare-except
        # The file content is not a valid UUID.
        return None


def write_installation_id_to_file(installation_id: str):
    try:
        _INSTALLATION_ID_PATH.parent.mkdir(
            exist_ok=True,
            parents=True,
        )
        _INSTALLATION_ID_PATH.write_text(
            f"{installation_id}{os.linesep}", encoding="utf8"
        )
    except:  # nosec  pylint: disable=bare-except
        # Do nothing even if the id could not be written to the file.
        ...


def get_installation_id() -> str:
    existing_id = get_installation_id_from_file()

    if existing_id is not None:
        return existing_id

    new_id = str(uuid4())

    write_installation_id_to_file(new_id)

    return new_id


def setup_telemetry():
    if disabled_by_atoti_plus() or disabled_by_environment_variable():
        return

    event = ImportEvent(
        operating_system=platform.platform(),
        installation_id=get_installation_id(),
        version=VERSION,
    )

    send_event_to_telemetry_service(event)
