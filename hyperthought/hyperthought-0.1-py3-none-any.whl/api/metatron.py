import os
import sys

import requests

up = os.path.dirname
# <submodule>/api/workflow/common.py
submodule_directory = up(up(up(__file__)))
sys.path.append(submodule_directory)

from api.base import GenericAPI, ERROR_THRESHOLD


class MetatronAPI(GenericAPI):
    """
    Metatron (parsers) API switchboard.

    Contains methods that correspond to endpoints for HyperThought™ parsers.

    Parameters
    ----------
    auth : auth.Authorization
        Authorization object used to get headers and cookies needed to call
        HyperThought endpoints.
    """

    def __init__(self, auth):
        super().__init__(auth)

    def get_parsers(self):
        """Get information on parsers available to the current user."""
        r = requests.get(
            url=f'{self._base_url}/api/metatron/parsers/',
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            verify=False,
        )

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)
