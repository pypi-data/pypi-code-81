from typing import Callable

from ..base_client import BaseClient

class ProcessInstanceHandler(BaseClient):

    def __init__(self, url: str, identity: Callable=None):
        super(ProcessInstanceHandler, self).__init__(url, identity)

    def terminate(self, process_instance_id: str, options: dict={}):
        path = f"/atlas_engine/api/v1/process_instances/{process_instance_id}/terminate"

        _ = self.do_put(path, {}, options)

        return True
