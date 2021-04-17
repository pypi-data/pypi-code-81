from kubernetes import client, config
from kubernetes.client import AppsV1Api,  CoreV1Api

from lgt_jobs.env import k8config
config.load_kube_config(k8config)

class KubernetesClientFactory:
    @staticmethod
    def create_core() -> CoreV1Api:
        kubernetes_client = client.CoreV1Api()
        kubernetes_client.api_client.configuration.verify_ssl = False
        kubernetes_client.api_client.configuration.ssl_ca_cert = None
        return kubernetes_client

    @staticmethod
    def create() -> AppsV1Api:
        kubernetes_client = client.AppsV1Api()
        kubernetes_client.api_client.configuration.verify_ssl = False
        kubernetes_client.api_client.configuration.ssl_ca_cert = None
        return kubernetes_client