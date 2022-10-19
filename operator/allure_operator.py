import os
import kopf
import yaml
import jinja2
from pathlib import Path
from kubernetes import client
from kubernetes import config
from kubernetes.client.rest import ApiException

@kopf.on.create("allure-docker-service.group", "v0.1", "operator")
def create_operator(name, namespace, spec, **kwargs):
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        template_path = "j2_template"
    else:
        template_path = "operator/j2_template"
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
    