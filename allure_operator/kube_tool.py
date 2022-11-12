import os
import yaml
from pathlib import Path
from kubernetes import client
from kubernetes import config

class KubeTool(object):
    """kubernetes api calls
    """
    def __init__(self) -> None:
        if not os.getenv("KUBERNETES_SERVICE_HOST"):
            kube_config = f"{str(Path.home())}/.kube/config"
            config.load_kube_config(kube_config)
        self._apps_api = client.AppsV1Api()
        self._core_api = client.CoreV1Api()
        self._network_api = client.NetworkingV1Api()

    def create_namespaced_persistent_volume_claim(self, namespace: str, body: yaml):
        return self._core_api.create_namespaced_persistent_volume_claim(namespace=namespace, body=body)

    def create_namespaced_config_map(self, namespace: str, body: yaml):
        return self._core_api.create_namespaced_config_map(namespace=namespace, body=body)

    def create_namespaced_deployment(self, namespace: str, body: yaml):
        return self._apps_api.create_namespaced_deployment(namespace=namespace, body=body)

    def create_namespaced_service(self, namespace: str, body: yaml):
        return self._core_api.create_namespaced_service(namespace=namespace, body=body)

    def create_namespaced_ingress(self, namespace: str, body: yaml):
        return self._network_api.create_namespaced_ingress(namespace=namespace, body=body)