"""Flywheel Core HTTP API Client."""
import copy
import functools
import os
import re
import typing as t

import orjson
from fw_http_client import HttpClient, HttpConfig
from memoization import cached
from packaging import version
from pydantic import root_validator

__all__ = ["CoreConfig", "CoreClient", "get_client"]

# regex to match api keys with (to extract the host if it's embedded)
API_KEY_RE = r"(?P<scheme>https?://)?(?P<host>[^:]+)(?P<port>:\d+)?:(?P<key>)"
# global cache of drone keys (device api keys acquired via drone secret)
DRONE_DEVICE_KEYS = {}


# pylint: disable=too-few-public-methods
class CoreConfig(HttpConfig):
    """Flywheel Core API connection and authentication configuration."""

    class Config:
        """Enable envvar config using prefix 'FW_CORE_'."""

        env_prefix = "fw_core_"

    api_key: t.Optional[str]
    url: t.Optional[str]
    drone_secret: t.Optional[str]
    device_type: t.Optional[str]
    device_label: t.Optional[str]
    auth_proxy: bool = False

    @root_validator
    @classmethod
    def validate_config(cls, values: dict) -> dict:
        """Validate core client configuration or raise AssertionError.

        Authentication options:
         * api_key prefixed with the site URL (from the profile page)
         * url and api_key without the site URL (from the device page)
         * url and drone_secret with device_label (auto-creates device key)
         * auth_proxy set to True, deferring auth to request-time
        """
        api_key, url = values.get("api_key"), values.get("url")
        assert api_key or url, "api_key or url required"
        # extract url from api_key assuming format "[scheme://]host[:port]:key"
        if not url:
            match = re.match(API_KEY_RE, t.cast(str, api_key))
            assert match, f"api_key with url expected (got {api_key!r})"
            scheme = match.group("scheme") or "https://"
            host = match.group("host")
            port = match.group("port") or ""
            url = f"{scheme}{host}{port}"
        # prefix url with https:// if only a domain/host is passed
        if not url.startswith("http"):
            url = f"https://{url}"
        # suffix url with /api path (if not already provided)
        url = url.rstrip("/")
        if not url.endswith("/api"):
            url = f"{url}/api"
        values["baseurl"] = url
        # require auth (unless it's deferred via auth_proxy)
        drone_secret = values.get("drone_secret")
        if not values.get("auth_proxy"):
            assert api_key or drone_secret, "api_key or drone_secret required"
        # default device_type to client_name and require device_label
        if drone_secret:
            if not values.get("device_type"):
                values["device_type"] = values.get("client_name")
            assert values.get("device_label"), "device_label required"
        return values


class CoreClient(HttpClient):
    """Flywheel Core HTTP API Client."""

    def __init__(self, config: t.Optional[CoreConfig] = None) -> None:
        """Initialize Core client from the config."""
        config = config or CoreConfig()
        super().__init__(config)
        if config.api_key:
            self.headers["Authorization"] = f"scitran-user {config.api_key}"
        elif config.drone_secret:
            self.headers["Authorization"] = self._get_device_key(config)

    def _get_device_key(self, config: CoreConfig) -> str:
        """Return device API key for the given drone_secret."""
        drone = (config.baseurl, config.device_type, config.device_label)
        if drone not in DRONE_DEVICE_KEYS:
            headers = {
                "X-Scitran-Auth": config.drone_secret,
                "X-Scitran-Method": config.device_type,
                "X-Scitran-Name": config.device_label,
            }
            device = self.get("/devices/self", headers=headers)
            DRONE_DEVICE_KEYS[drone] = device.key
        return DRONE_DEVICE_KEYS[drone]

    # pylint: disable=arguments-differ
    def request(self, method: str, url: str, **kwargs):
        """Send Flywheel Core API request and return the response."""
        # enable setting authorization header with an str auth kwarg
        if isinstance(kwargs.get("auth"), str):
            headers = kwargs.setdefault("headers", {})
            headers["Authorization"] = kwargs.pop("auth")
        return super().request(method, url, **kwargs)

    @functools.cached_property
    def config(self) -> dict:
        """Return Core's configuration."""
        return self.get("/config")

    @functools.cached_property
    def version(self) -> t.Optional[str]:
        """Return Core's release version."""
        return self.get("/version").release

    @functools.cached_property
    def status(self) -> dict:
        """Return the client's auth status."""
        status = self.get("/auth/status")
        if status.is_device:
            status["info"] = self.get(f"/devices/{status.origin.id}")
        else:
            status["info"] = self.get("/users/self")
        return status

    def check_feature(self, feature: str) -> bool:
        """Return True if Core has the given feature and it's enabled."""
        return bool(self.config.features.get(feature))  # type: ignore

    def check_version(self, min_ver: str) -> bool:
        """Return True if Core's version is greater or equal to 'min_ver'."""
        if not self.version:
            # assume latest on dev deployments without a version
            return True
        return version.parse(self.version) >= version.parse(min_ver)

    def upload(
        self,
        filepath: str,
        metadata: dict,
        method: str = "label",
        fill: bool = False,
    ) -> dict:
        """Upload a file using the label or reaper /upload endpoint."""
        assert method in ("label", "reaper"), f"Invalid upload method {method!r}"
        endpoint = f"/upload/{method}"
        filename, metadata = get_upload_info(filepath, metadata, method, fill)
        with open(filepath, "rb") as file:
            if self.config.get("signed_url"):
                payload = {"filenames": [filename], "metadata": metadata}
                upload = self.post(endpoint, params={"ticket": ""}, json=payload)
                self.put(upload.urls[filename], data=file)
                response = self.post(endpoint, params={"ticket": upload.ticket})
            else:
                meta = orjson.dumps(metadata)
                response = self.post(endpoint, files={filename: file, "metadata": meta})
        return response


@cached
def get_client(**kwargs: t.Any) -> CoreClient:
    """Return (cached) CoreClient configured via kwargs."""
    return CoreClient(CoreConfig(**kwargs))


def get_upload_info(
    filepath: str, meta: dict, method: str, fill: bool
) -> t.Tuple[str, dict]:
    """Return (filename, meta) tuple for given upload parameters.

    Core expects label- and reaper uploads as file forms with two files:
      * filename: with the actual file contents
      * metadata: json describing hierarchy placement and additional meta

    Core requires that the metadata has:
      * group._id set to a string ("" allowed)
      * project.label set to a string ("" allowed)
      * subject - if present - embedded under the session
      * uids in case of reaper uploads:
        * session.uid set to a string ("" allowed)
        * acquisition.uid set to a string if the acquisition is present ("" allowed)
      * the filename referenced on some hierarchy level (project or below)

    This function helps getting a correct (filename, metadata) pair where the
    filename is set appropriately if it was present in the metadata, or defaults
    to using the file's basename while making sure it is referenced in the meta.
    The subject - if present - is automatically embedded into the session.

    If fill=True then group._id and project.label, session.uid and acquisition.uid
    are auto-populated with empty strings as necessary to avoid rejected uploads.
    """
    meta = copy.deepcopy(meta)
    # populate group._id and project.label if not set
    if fill:
        if not meta.setdefault("group", {}).get("_id"):
            meta["group"]["_id"] = ""
        if not meta.setdefault("project", {}).get("label"):
            meta["project"]["label"] = ""
    # try to get filename from the meta (going bottom up, looking for files)
    filename = meta.get("file", {}).get("name")
    for level in ("acquisition", "session", "subject", "project"):
        if not meta.get(level):
            continue
        cont = meta[level]
        if filename:
            # using fw-meta file info
            cont["files"] = [meta.pop("file")]
            break
        if cont.get("files"):
            filename = cont["files"][0].get("name")
            break
    # use basename by default and set it in the meta at acquisition level
    if not filename:
        filename = os.path.basename(filepath)
        files = meta.setdefault("acquisition", {}).setdefault("files", [{}])
        files[0]["name"] = filename
    # embed subject meta under session
    if "subject" in meta:
        meta.setdefault("session", {})["subject"] = meta.pop("subject")
    # populate session.uid and acquisition.uid on reaper uploads
    if fill and method == "reaper":
        meta.setdefault("session", {}).setdefault("uid", "")
        if "acquisition" in meta:  # acquisition may be omitted
            meta.setdefault("acquisition", {}).setdefault("uid", "")
    return filename, meta
