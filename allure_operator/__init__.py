import kopf
from kubernetes.client.rest import ApiException
from allure_operator.j2_tool import J2Template
from allure_operator.kube_tool import KubeTool
from allure_operator.allure_spec import AllureSpec

@kopf.on.create("allure-docker-service.group", "v1", "allureopt")
def create_allure(namespace: str, spec: dict, **kwargs):
    """obj create hook

    Args:
        namespace (str): namespace
        spec (dict): spec dict

    Raises:
        kopf.PermanentError: ingress data err
        kopf.PermanentError: nodeport data err
        kopf.PermanentError: k8s api call err

    Returns:
        dict: status dict
    """
    namespace = namespace
    allure_info = AllureSpec(spec=spec)
    j2_template = J2Template(allure_info=allure_info)
    kube_tool = KubeTool()
    if allure_info.expose_type == "nodeport":
        if allure_info.nodeport_api_port > 0 and allure_info.nodeport_ui_port > 0 and len(allure_info.nodeport_ext_ip) > 0:            
            allure_nodeport_yaml = j2_template.allure_nodeport_yaml
            kopf.adopt(allure_nodeport_yaml)
        else:
            raise kopf.PermanentError("nodeport data wrong")
    if allure_info.expose_type == "ingress":
        if len(allure_info.ingress_fqdn) > 0:
            allure_service_yaml = j2_template.allure_service_yaml
            allure_ingress_yaml = j2_template.allure_ingress_yaml
            kopf.adopt(allure_service_yaml)
            kopf.adopt(allure_ingress_yaml)
        else:
            raise kopf.PermanentError("ingress data wrong") 
    if len(allure_info.loop_pytest_ver) > 0 and allure_info.loop_timer > 0:
        loop_pytest_deployment_yaml = j2_template.loop_pytest_deployment_yaml
        kopf.adopt(loop_pytest_deployment_yaml)
    allure_pvc_yaml = j2_template.allure_pvc_yaml
    allure_configmap_api_yaml = j2_template.allure_configmap_api_yaml
    allure_configmap_ui_yaml = j2_template.allure_configmap_ui_yaml
    allure_deployment_yaml = j2_template.allure_deployment_yaml
    kopf.adopt(allure_pvc_yaml)
    kopf.adopt(allure_configmap_api_yaml)
    kopf.adopt(allure_configmap_ui_yaml)
    kopf.adopt(allure_deployment_yaml)
    try:
        allure_pvc = kube_tool.create_namespaced_persistent_volume_claim(namespace=namespace, body=allure_pvc_yaml)
        allure_configmap_api = kube_tool.create_namespaced_config_map(namespace=namespace, body=allure_configmap_api_yaml) 
        allure_configmap_ui = kube_tool.create_namespaced_config_map(namespace=namespace, body=allure_configmap_ui_yaml)
        allure_deployment = kube_tool.create_namespaced_deployment(namespace=namespace, body=allure_deployment_yaml)
        if allure_info.expose_type == "nodeport":
            allure_nodeport = kube_tool.create_namespaced_service(namespace=namespace, body=allure_nodeport_yaml)
        if allure_info.expose_type == "ingress":
            allure_service = kube_tool.create_namespaced_service(namespace=namespace, body=allure_service_yaml)
            allure_ingress = kube_tool.create_namespaced_ingress(namespace=namespace, body=allure_ingress_yaml)
        if len(allure_info.loop_pytest_ver) > 0 and allure_info.loop_timer > 0:
            loop_pytest_deployment_yaml
            loop_pytest_deployment = kube_tool.create_namespaced_deployment(namespace=namespace, body=loop_pytest_deployment_yaml)
        return {
            "PVC": allure_pvc.metadata.name,
            "CONFIGMAP_API": allure_configmap_api.metadata.name,
            "CONFIGMAP_UI": allure_configmap_ui.metadata.name,
            "ALLURE_DEPLOYMENT": allure_deployment.metadata.name,
            "UI": allure_info.ui_url,
            "LOOP_PYTEST_DEPLOYMENT": loop_pytest_deployment.metadata.name,
            "LOOP_TIMER": allure_info.loop_timer,
            "LOOP_PYTEST_VER": allure_info.loop_pytest_ver,
            }
    except ApiException as e:
        raise kopf.PermanentError("Exception: %s\n" % e)
