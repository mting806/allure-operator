from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar

@dataclass
class AllureSpec(object):
    spec: InitVar
    expose_type: str = field(init=False)
    storage_class: str = field(init=False)
    loop_timer: int = field(init=False)
    loop_pytest: bool = field(init=False)
    loop_pytest_image: str = field(init=False)
    pvc_size: str = field(init=False)
    nodeport_ext_ip: str  = None
    nodeport_api_port: int  = None
    nodeport_ui_port: int  = None
    ingress_fqdn: str  = None
    api_public_url: str = field(init=False)
    ui_url: str = field(init=False)
    def __post_init__(self, spec: dict):
        self.expose_type = spec["expose_type"]
        self.storage_class = spec["storage_class"]
        self.loop_timer = spec["loop_timer"]
        self.loop_pytest = spec["loop_pytest"]
        self.loop_pytest_image = spec["loop_pytest_image"] 
        self.pvc_size = spec["pvc_size"]
        self.pytest_cmd = spec["pytest_cmd"]
        if self.expose_type == "nodeport":
            self.nodeport_ext_ip = spec["nodeport_ext_ip"]
            self.nodeport_api_port = spec["nodeport_api_port"]
            self.nodeport_ui_port = spec["nodeport_ui_port"]
            self.api_public_url = f"http://{self.nodeport_ext_ip}:{self.nodeport_api_port}"
            self.ui_url = f"http://{self.nodeport_ext_ip}:{self.nodeport_ui_port}"
        if self.expose_type == "ingress":
            self.ingress_fqdn = spec["ingress_fqdn"]  
            self.api_public_url = f"http://{self.ingress_fqdn}"
            self.ui_url = f"http://{self.ingress_fqdn}"   
