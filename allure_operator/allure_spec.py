from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar

@dataclass
class AllureSpec(object):
    spec: InitVar
    expose_type: str = field(init=False)
    storage_class: str = field(init=False)
    nodeport_ext_ip: str = field(init=False)
    nodeport_api_port: int = field(init=False)
    nodeport_ui_port: int = field(init=False)
    ingress_fqdn: str = field(init=False)
    api_public_url: str = field(init=False)
    ui_url: str = field(init=False)
    def __post_init__(self, spec: dict):
        self.expose_type = spec["expose_type"]
        self.storage_class = spec["storage_class"]
        self.nodeport_ext_ip = spec["nodeport_ext_ip"]
        self.nodeport_api_port = spec["nodeport_api_port"]
        self.nodeport_ui_port = spec["nodeport_ui_port"]
        self.ingress_fqdn = spec["ingress_fqdn"]   
        if self.expose_type == "nodeport":
            self.api_public_url = f"http://{self.nodeport_ext_ip}:{self.nodeport_api_port}"
            self.ui_url = f"http://{self.nodeport_ext_ip}:{self.nodeport_ui_port}"
        if self.expose_type == "ingress":
            self.api_public_url = f"http://{self.ingress_fqdn}"
            self.ui_url = f"http://{self.ingress_fqdn}"   
