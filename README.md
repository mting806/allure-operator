# allure-operator

Kubernetes operator for deploy [allure-docker-service](https://github.com/fescobar/allure-docker-service)  

## Kubernetes requirements

[storage_class](https://kubernetes.io/docs/concepts/storage/storage-classes/) that support ReadWriteMany is required, for example [nfs-subdir-external-provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)  

[ingress-nginx](https://github.com/kubernetes/ingress-nginx) is required for ingress expose

## Installation

```
kubectl apply -f https://raw.githubusercontent.com/mting806/allure-operator/main/kube_files/allure-operator-all.yaml
```

It will create below items:
<ol>
  <li>crd <strong>allureopts.allure-docker-service.group:v1</strong></li>
  <li>namespace <strong>allure</strong></li>
  <li>serviceaccount <strong>allureopt</strong> in namespace <strong>allure</strong></li>
  <li>clusterrolebinding <strong>allureopt</strong></li>
  <li>deployment <strong>allureopt</strong> in namespace <strong>allure</strong></li>
</ol>

## Usage

allure-opt monitor the crd in namespace <strong>allure</strong>, it will create allure object and loop pytest by definition of <strong>allureopts.allure-docker-service.group:v1</strong> api 

### Configuration

allure.yaml  
```
apiVersion: allure-docker-service.group/v1
kind: AllureOpt
metadata:
  name: allure
spec:
#  expose_type: nodeport
  expose_type: ingress
  nodeport_api_port: 30008
  nodeport_ui_port: 30009
  nodeport_ext_ip: 192.168.88.70
  keep_history_num: 200
  ingress_fqdn: allure.test
  storage_class: nfs-client
  pvc_size: 1Gi
  loop_timer: 30
  loop_pytest: yes
#  loop_pytest: no
  loop_pytest_image: "mting/loop_pytest:0.4" 
  pytest_cmd: "python -m pytest test.py" 
```

#### Mandatory parameters:    
```
expose_type(string)(immutable): "ingress" or "nodeport"  
storage_class(string)(immutable): the storage class name  
loop_timer(int)(immutable): pytest loop timer in second  
loop_pytest_image(string): pytest image   
pvc_size(string)(immutable): pvc size
keep_history_num(string)(immutable): keep test history number
loop_pytest(bool): "yes" or "no" run loop pytest or not  
pytest_cmd(string): pytest command in pytest_loop deployment
```
#### Optional parameters:  
```
nodeport_api_port(integer)(immutable): api nodeport, needed for nodeport expose_type  
nodeport_ui_port(integer)(immutable): ui nodeport, needed for nodeport expose_type  
nodeport_ext_ip(string)(immutable): ip address for nodeport, needed for nodeport expose_type   
ingress_fqdn(string)(immutable): ingress fqdn, needed for ingress expose_type  
```

### Deploy allure object

```
kubectl apply -f allure.yaml -n allure
```

It will create below items in namespace <strong>allure</strong>:  

<ol>
  <li>configmap for allure-docker-service api</li>
  <li>configmap for allure-docker-service ui</li>
  <li>nodeport service for allure-docker-service api and allure-docker-service ui</li>
  <li>service for allure-docker-service api and allure-docker-service ui</li>
  <li>ingress to item 4</li>
  <li>allure deployment</li>
  <li>loop pytest deployment</li>
</ol>

```
/ # kubectl get allure -n allure
NAME     TYPE      PVC_SIZE   ALLURE_DEPLOYMENT   UI                   LOOP_PYTEST_DEPLOYMENT   LOOP_TIMER   LOOP_PYTEST   LOOP_PYTEST_IMAGE       PYTEST_CMD
allure   ingress   1Gi        allure-deployment   http://allure.test   loop-pytest-deployment   30           false         mting/loop_pytest:0.4   python -m pytest test.py
```

### Update allure object

pytest loop run or not,  
pytest image,  
pytest command  
could be changed by

```
loop_pytest(bool): "yes" or "no" 
loop_pytest_image(string): pytest image 
pytest_cmd(string): pytest command in pytest_loop deployment
```
then
```
kubectl apply -f allure.yaml -n allure
```

Or direcy edit deployment
```
kubectl edit depolyment loop-pytest-deployment -n allure
```

### Delete allure object

```
kubectl delete -f allure.yaml -n allure
```

### Cleanup all
```
kubectl delete -f https://raw.githubusercontent.com/mting806/allure-operator/main/kube_files/allure-operator-all.yaml
```