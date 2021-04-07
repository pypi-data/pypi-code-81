from typing import Optional
from cannerflow.request import CannerRequest
from cannerflow.saved_query import SavedQuery
from cannerflow.query import Query
from cannerflow.file import File

__all__ = ["Workspace"]

class Workspace(object):
    def __init__(
        self,
        endpoint: str,
        workspace_id: str,
        headers: Optional[dict] = None,
        replaceLocalhostString: Optional[dict] = None,
    ):
        self.replaceLocalhostString = replaceLocalhostString
        self.endpoint = self._replace_localhost(endpoint)
        self.headers = headers
        self.workspace_id = workspace_id
        request = CannerRequest(
            headers=headers,
            endpoint=self.endpoint
        )
        self.request = request
        self.saved_query = SavedQuery(
            request=request,
            workspace_id=workspace_id
        )
        self.file = File(
            request=request,
            workspace_id=workspace_id,
            replaceLocalhostString=replaceLocalhostString
        )
    def gen_query(self, sql: str, cache_refresh: bool, cache_ttl: int, data_format: str, fetch_by: str):
        return Query(
            request=self.request,
            workspace_id=self.workspace_id,
            sql=sql,
            cache_refresh=cache_refresh,
            cache_ttl=cache_ttl,
            data_format=data_format,
            fetch_by=fetch_by
        )

    def _replace_localhost(self, url: str):
        if (self.replaceLocalhostString != None):
            return url.replace('localhost', self.replaceLocalhostString).replace('127.0.0.1', self.replaceLocalhostString)
        else:
            return url