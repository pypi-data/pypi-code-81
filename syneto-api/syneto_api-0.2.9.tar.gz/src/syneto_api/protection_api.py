import os
from .api_client import APIClientBase


class Protection(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(url_base or os.environ.get("PROTECTION_SERVICE", ""), **kwargs)

    def get_policies(self):
        return self.get_request("/policies")

    def get_policy(self, id):
        return self.get_request("/policies/{id}", id=id)

    def create_policy(
        self,
        policy_name: str,
        pool_name: str = None,
        alert_enabled: bool = True,
        rules: list = None,
    ):
        body = {
            "policyName": policy_name,
            "poolName": pool_name,
            "alertEnabled": alert_enabled,
            "rules": rules or [],
        }
        return self.post_request("/policies", body=body)

    def patch_policy(
        self,
        id: str,
        policy_name: str = None,
        pool_name: str = None,
        alert_enabled: bool = None,
        rules: list = None,
    ):
        body = {}

        if policy_name is not None:
            body["policyName"] = policy_name
        if pool_name is not None:
            body["poolName"] = pool_name
        if alert_enabled is not None:
            body["alertEnabled"] = alert_enabled
        if rules is not None:
            body["rules"] = rules

        return self.patch_request("/policies/{id}", id=id, body=body)

    def delete_policy(self, id):
        return self.get_request("/policies/{id}", id=id)

    def get_replication_hosts(self):
        return self.get_request("/hosts")

    def get_replication_host(self, id):
        return self.get_request("/hosts/{id}", id=id)

    def create_replication_host(self, body):
        return self.post_request("/hosts", body=body)

    def delete_replication_host(self, id):
        return self.delete_request("/hosts/{id}", id=id)

    def patch_replication_host(self, id, body):
        return self.patch_request("/hosts/{id}", id=id, body=body)

    def get_protected_vms(self):
        return self.get_request("/vms")

    def get_protected_vm(self, vm_syn_id: str):
        return self.get_request("/vms/{vm_syn_id}", vm_syn_id=vm_syn_id)

    def create_external_vm_protection_job(self, config):
        body = {"config": config}
        return self.post_request("/jobs/protect-external-vm", body=body)

    def create_local_vm_protection_job(self, config):
        body = {"config": config}
        return self.post_request("/jobs/protect-local-vm", body=body)

    def create_local_vm_replication_job(self, config):
        body = {"config": config}
        return self.post_request("/jobs/replicate-local-vm", body=body)

    def post_vm_recovery_point(self, vm_syn_id: str, job_id: str):
        return self.post_request(
            "/vms/recovery-points", body={"synId": vm_syn_id, "jobId": job_id}
        )
