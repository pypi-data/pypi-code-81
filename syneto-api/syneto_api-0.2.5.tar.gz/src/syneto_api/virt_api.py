import os
from .api_client import APIClientBase


class Virtualization(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(
            url_base or os.environ.get("VIRTUALIZATION_SERVICE", ""), **kwargs
        )

    def wait_for_task(self, task_syn_id):
        while True:
            try:
                result = self.get_request(
                    "/vmware/tasks/{task_syn_id}", task_syn_id=task_syn_id
                )
                if result["state"] in ["success"]:
                    return
            except APIException as e:
                raise

    def get_hypervisors(self):
        return self.get_request("/hypervisors")

    def get_vms(self):
        return self.get_request("/vms")

    def get_vmware_hosts(self):
        return self.get_request("/vmware/hosts")

    def get_vmware_datastores(self):
        return self.get_request("/vmware/datastores")

    def get_vm_snapshot(self, vm_syn_id: str, snapshot_name: str):
        snapshots = self.get_request("/vms/{vm_syn_id}/snapshots", vm_syn_id=vm_syn_id)
        return next((snap for snap in snapshots if snap["name"] == snapshot_name), None)

    def create_vm_snapshot(
        self,
        vm_syn_id: str,
        snapshot_name: str,
        quiesce: bool = True,
        dumpmem: bool = False,
    ):
        body = {
            "name": snapshot_name,
            "description": snapshot_name,
            "quiesce": quiesce,
            "dumpmem": dumpmem,
        }
        task = self.post_request(
            "/vms/{vm_syn_id}/snapshots",
            vm_syn_id=vm_syn_id,
            query_args={"wait_for_task": "false"},
            body=body,
        )
        self.wait_for_task(task["synId"])
        return self.get_vm_snapshot(vm_syn_id, snapshot_name)

    def delete_vm_snapshot(self, vm_syn_id, snapshot_ref_id):
        task = self.delete_request(
            "/vms/{vm_syn_id}/snapshots",
            vm_syn_id=vm_syn_id,
            query_args={"snapshot_ref_id": snapshot_ref_id, "wait_for_task": "true"},
            success_codes=[200, 202, 204],
        )
        self.wait_for_task(task["synId"])

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
