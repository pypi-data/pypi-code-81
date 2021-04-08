from dataclasses import dataclass
from typing import Callable
from ..base_client import BaseClient

@dataclass
class ApplicationInfo:
    name: str
    packageName: str
    version: str
    authorityUrl: str
    allowAnonymousRootAccess: str
    extraInfo: dict


class ApplicationInfoHandler(BaseClient):

    def __init__(self, url: str, identity: Callable=None):
        super(ApplicationInfoHandler, self).__init__(url, identity)

    def info(self) -> ApplicationInfo:
        json_data = self.do_get('/atlas_engine/api/v1/info')

        info = ApplicationInfo(**json_data)

        return info

    def authority(self) -> str:
        json_data = self.do_get('/atlas_engine/api/v1/authority')

        return json_data