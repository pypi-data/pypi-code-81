import os
import sys

import requests

up = os.path.dirname
# <submodule>/api/workflow/common.py
submodule_directory = up(up(up(__file__)))
sys.path.append(submodule_directory)

from api.base import GenericAPI, ERROR_THRESHOLD


class GroupsAPI(GenericAPI):
    """
    Groups API switchboard.

    Contains methods that correspond to endpoints for HyperThought™ groups.

    Parameters
    ----------
    auth : auth.Authorization
        Authorization object used to get headers and cookies needed to call
        HyperThought endpoints.
    """

    NAME_FIELD = 'name'

    def __init__(self, auth):
        super().__init__(auth)

    def get_groups(self):
        """Get groups available to the current user."""
        r = requests.get(
            url='{}/api/groups/'.format(self._auth.get_base_url()),
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            verify=False,
        )

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)

    def get_name_field(self):
        """
        Get the key name of the field containing the group name.

        This will be a name in the content section of a group document.
        """
        return self.NAME_FIELD
