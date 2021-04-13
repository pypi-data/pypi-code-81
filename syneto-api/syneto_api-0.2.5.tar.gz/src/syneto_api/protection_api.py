import os
from .api_client import APIClientBase


class Protection(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(url_base or os.environ.get("PROTECTION_SERVICE", ""), **kwargs)

    def get_policies(self):
        return self.get_request("/policies")

    def get_protected_vms(self):
        return self.get_request("/vms")

    def get_jobs(self):
        return self.get_request("/jobs")

    def get_job(self, id):
        return self.get_request("/jobs/{}", id)

    def patch_job(self, id, body):
        return self.patch_request("/jobs", query_args={"id": id}, body=body)

    def remove_job(self, id):
        return self.delete_request("/jobs", query_args={"id": id})

    def create_external_vm_protection_job(self, config):
        body = {"config": config}
        return self.post_request("/jobs/protect-external-vm", body=body)

    def create_local_vm_protection_job(self, config):
        body = {"config": config}
        return self.post_request("/jobs/protect-local-vm", body=body)

    def create_local_vm_replication_job(self, config):
        body = {"config": config}
        return self.post_request("/jobs/replicate-local-vm", body=body)

    def get_replication_hosts(self):
        return self.get_request("/hosts")

    def get_replication_host(self, id):
        return self.get_request("/hosts/{}", id)

    def create_replication_host(self, payload):
        return self.post_request("/hosts", body=payload)

    def remove_replication_host(self, id):
        return self.delete_request("/hosts", query_args={"id": id})

    def patch_replication_host(self, id, payload):
        return self.patch_request("/hosts", query_args={"id": id}, body=payload)

    def get_protected_vm(self, vm_syn_id: str):
        return self.get_request("/vms/{vm_syn_id}", vm_syn_id=vm_syn_id)

    def post_vm_recovery_point(self, vm_syn_id: str, job_id: str):
        return self.post_request(
            "/vms/recovery-points", body={"synId": vm_syn_id, "jobId": job_id}
        )
