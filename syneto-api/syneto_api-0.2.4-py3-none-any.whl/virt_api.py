import os
from .api_client import APIClientBase


class Virtualization(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(
            url_base or os.environ.get("VIRTUALIZATION_SERVICE", ""), **kwargs
        )

    def get_hypervisors(self):
        return self.get_request("/hypervisors")

    def get_vms(self):
        return self.get_request("/vms")

    def get_vmware_hosts(self):
        return self.get_request("/vmware/hosts")

    def get_vmware_datastores(self):
        return self.get_request("/vmware/datastores")

    def get_image_repository(self):
        return self.get_request("/image-repository")

    def create_nas_datastore(self, server: str, mountpoint: str, hosts_syn_ids=None):
        return self.post_request(
            "/vmware/datastores",
            body={
                "server": server,
                "mountpoint": mountpoint,
                "hosts_syn_ids": hosts_syn_ids if hosts_syn_ids else [],
            },
        )

    def delete_nas_datastore(self, syn_id: str = None, mountpoint: str = None):
        return self.delete_request(
            "/vmware/datastores",
            query_args={"datastore_syn_id": syn_id, "datastore_mountpoint": mountpoint},
        )
