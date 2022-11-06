import os
import kopf
import yaml
import jinja2
from pathlib import Path
from kubernetes import client
from kubernetes import config
from kubernetes.client.rest import ApiException

@kopf.on.create("allure-docker-service.group", "v1", "allureopt")
def create_allure(name, namespace, spec, **kwargs):
#    if os.getenv("KUBERNETES_SERVICE_HOST"):
#        template_path = "j2_template"
#    else:
#        template_path = "allure_operator/j2_template"
    template_path = "allure_operator/j2_template"
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
    name = name
    namespace = namespace
    expose_type = spec["expose_type"]
    allure_info = {}
    allure_pv_template = template_env.get_template("allure_pv.j2")
    allure_pvc_template = template_env.get_template("allure_pvc.j2")
    allure_configmap_api_template = template_env.get_template("allure_configmap_api.j2")
    allure_configmap_ui_template = template_env.get_template("allure_configmap_ui.j2")
    allure_deployment_template = template_env.get_template("allure_deployment.j2")
    allure_nodeport_template = template_env.get_template("allure_nodeport.j2")
    if expose_type == "nodeport":
        nodeport_ext_ip = spec["nodeport_ext_ip"]
        nodeport_api_port = spec["nodeport_api_port"]
        nodeport_ui_port = spec["nodeport_ui_port"]
        if nodeport_api_port > 0 and nodeport_ui_port > 0 and len(nodeport_ext_ip) > 0:            
            ui_url = f"http://{nodeport_ext_ip}:{nodeport_ui_port}"
            allure_info["nodeport_api_port"] = nodeport_api_port
            allure_info["nodeport_ui_port"] = nodeport_ui_port
            allure_info["api_public_url"] = f"http://{nodeport_ext_ip}:{nodeport_api_port}"
            allure_nodeport_output = allure_nodeport_template.render(allure_info=allure_info)
            allure_nodeport_yaml = yaml.safe_load(allure_nodeport_output)
            kopf.adopt(allure_nodeport_yaml)
        else:
            raise kopf.PermanentError("nodeport data wrong")
    allure_pv_output = allure_pv_template.render(allure_info=allure_info)
    allure_pvc_output = allure_pvc_template.render(allure_info=allure_info)
    allure_configmap_api_output = allure_configmap_api_template.render(allure_info=allure_info)
    allure_configmap_ui_output = allure_configmap_ui_template.render(allure_info=allure_info)
    allure_deployment_output = allure_deployment_template.render(allure_info=allure_info)
    allure_pv_yaml = yaml.safe_load(allure_pv_output)
    allure_pvc_yaml = yaml.safe_load(allure_pvc_output)
    allure_configmap_api_yaml = yaml.safe_load(allure_configmap_api_output)
    allure_configmap_ui_yaml = yaml.safe_load(allure_configmap_ui_output)
    allure_deployment_yaml = yaml.safe_load(allure_deployment_output)
    kopf.adopt(allure_pvc_yaml)
    kopf.adopt(allure_configmap_api_yaml)
    kopf.adopt(allure_configmap_ui_yaml)
    kopf.adopt(allure_deployment_yaml)
    if not os.getenv("KUBERNETES_SERVICE_HOST"):
        kube_config = f"{str(Path.home())}/.kube/config"
        config.load_kube_config(kube_config)
    apps_api = client.AppsV1Api()
    core_api = client.CoreV1Api()
    try:
        allure_pv = core_api.create_persistent_volume(body=allure_pv_yaml)
        allure_pvc = core_api.create_namespaced_persistent_volume_claim(namespace=namespace, body=allure_pvc_yaml)
        allure_configmap_api = core_api.create_namespaced_config_map(namespace=namespace, body=allure_configmap_api_yaml) 
        allure_configmap_ui = core_api.create_namespaced_config_map(namespace=namespace, body=allure_configmap_ui_yaml)
        allure_deployment = apps_api.create_namespaced_deployment(namespace=namespace, body=allure_deployment_yaml)
        if expose_type == "nodeport":
            allure_nodeport = core_api.create_namespaced_service(namespace=namespace, body=allure_nodeport_yaml)
        return {
            "PV": allure_pv.metadata.name,
            "PVC": allure_pvc.metadata.name,
            "CONFIGMAP_API": allure_configmap_api.metadata.name,
            "CONFIGMAP_UI": allure_configmap_ui.metadata.name,
            "DEPLOYMENT": allure_deployment.metadata.name,
            "UI": ui_url
            }
    except ApiException as e:
        raise kopf.PermanentError("Exception: %s\n" % e)

@kopf.on.delete("allure-docker-service.group", "v1", "allureopt")
def delete_allure(name, namespace, spec, **kwargs):
    core_api = client.CoreV1Api()
    try:
        core_api.delete_persistent_volume(name="allure-persistent-volume")
    except ApiException as e:
        raise kopf.PermanentError("Exception: %s\n" % e)