import jinja2
import yaml
from allure_operator.allure_spec import AllureSpec

class J2Template(object):
    """render yaml

    Args:
        allure_info (dict): allure_info dict

    Attributes:
        allure_nodeport_yaml (yaml): nodeport yaml
        allure_service_yaml (yaml): service yaml
        allure_ingress_yaml (yaml): ingress yaml
        allure_pvc_yaml (yaml): pvc yaml
        allure_configmap_api_yaml (yaml): configmap api yaml
        allure_configmap_ui_yaml (yaml): configmap ui yaml
        allure_deployment_yaml (yaml): deployment yaml

    """
    allure_nodeport_yaml: yaml
    allure_service_yaml: yaml
    allure_ingress_yaml: yaml
    allure_pvc_yaml: yaml
    allure_configmap_api_yaml: yaml
    allure_configmap_ui_yaml: yaml 
    allure_deployment_yaml: yaml
    loop_pytest_deployment_yaml: yaml
    def __init__(
        self,
        allure_info: AllureSpec
        ):
        template_path = "allure_operator/j2_template"
        template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
        allure_pvc_template = template_env.get_template("allure_pvc.j2")
        allure_configmap_api_template = template_env.get_template("allure_configmap_api.j2")
        allure_configmap_ui_template = template_env.get_template("allure_configmap_ui.j2")
        allure_deployment_template = template_env.get_template("allure_deployment.j2")
        allure_nodeport_template = template_env.get_template("allure_nodeport.j2")
        allure_service_template = template_env.get_template("allure_service.j2")
        allure_ingress_template = template_env.get_template("allure_ingress.j2")
        loop_pytest_deployment_template = template_env.get_template("loop_pytest_deployment.j2")
        allure_nodeport_output = allure_nodeport_template.render(allure_info=allure_info)
        allure_service_output = allure_service_template.render(allure_info=allure_info)
        allure_ingress_output = allure_ingress_template.render(allure_info=allure_info)
        allure_pvc_output = allure_pvc_template.render(allure_info=allure_info)
        allure_configmap_api_output = allure_configmap_api_template.render(allure_info=allure_info)
        allure_configmap_ui_output = allure_configmap_ui_template.render(allure_info=allure_info)
        allure_deployment_output = allure_deployment_template.render(allure_info=allure_info)
        loop_pytest_deployment_output = loop_pytest_deployment_template.render(allure_info=allure_info)
        self.allure_nodeport_yaml = yaml.safe_load(allure_nodeport_output)
        self.allure_service_yaml = yaml.safe_load(allure_service_output)
        self.allure_ingress_yaml = yaml.safe_load(allure_ingress_output)
        self.allure_pvc_yaml = yaml.safe_load(allure_pvc_output)
        self.allure_configmap_api_yaml = yaml.safe_load(allure_configmap_api_output)
        self.allure_configmap_ui_yaml = yaml.safe_load(allure_configmap_ui_output)
        self.allure_deployment_yaml = yaml.safe_load(allure_deployment_output)
        self.loop_pytest_deployment_yaml = yaml.safe_load(loop_pytest_deployment_output)
