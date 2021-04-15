import os
import sys

import requests

up = os.path.dirname
# <submodule>/api/workflow/common.py
submodule_directory = up(up(up(__file__)))
sys.path.append(submodule_directory)

from api.base import GenericAPI, ERROR_THRESHOLD


class ProjectsAPI(GenericAPI):
    """
    Projects API switchboard.

    Contains methods that correspond to endpoints for HyperThought™ projects.

    Parameters
    ----------
    auth : auth.Authorization
        Authorization object used to get headers and cookies needed to call
        HyperThought endpoints.
    """

    NAME_FIELD = 'title'

    def __init__(self, auth):
        super().__init__(auth)

    def get_projects(self):
        """Get projects available to the current user."""
        r = requests.get(
            url='{}/api/projects/project/'.format(self._auth.get_base_url()),
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
        Get the key name of the field containing the project name.

        This will be a name in the content section of a project document.
        """
        return self.NAME_FIELD
