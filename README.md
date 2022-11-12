# allure-operator

Kubernetes operator for deploy [allure-docker-service](https://github.com/fescobar/allure-docker-service)  

## Kubernetes requirements

[storage_class](https://kubernetes.io/docs/concepts/storage/storage-classes/) that support ReadWriteMany is required, for example [nfs-subdir-external-provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner) . 

[ingress-nginx](https://github.com/kubernetes/ingress-nginx) is required for ingress expose

## Installation

```
kubectl apply -f https://raw.githubusercontent.com/mting806/allure-operator/main/kube_files/allure-operator-crd.yaml
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

allure-opt monitor the crd in namespace <strong>allure</strong>, it will create allure-docker-service by definition of <strong>allureopts.allure-docker-service.group:v1</strong> api 

deploy allure-docker-server 

```
kubectl apply -f allure.yaml -n allure
```

delete allure-docker-server 

```
kubectl delete -f allure.yaml -n allure
```

allure.yaml  
```
apiVersion: allure-docker-service.group/v1
kind: AllureOpt
metadata:
  name: allure
spec:
#  expose_type: nodeport
  expose_type: ingress
  storage_class: standard
  nodeport_api_port: 30008
  nodeport_ui_port: 30009
  nodeport_ext_ip: 192.168.88.70
  ingress_fqdn: allure.test
  
```

### Mandatory parameters:    

expose_type(string): "ingress" or "nodeport"  
storage_class(string): the storage class name  

### Optional parameters:  

nodeport_api_port(integer): api nodeport, needed for nodeport expose_type  
nodeport_ui_port(integer): ui nodeport, needed for nodeport expose_type  
nodeport_ext_ip(string): ip address for nodeport, needed for nodeport expose_type   
ingress_fqdn(string): ingress fqdn, needed for ingress expose_type  

It will create below items in namespace <strong>allure</strong>:  

<ol>
  <li>configmap for allure-docker-service api</li>
  <li>configmap for allure-docker-service ui</li>
  <li>nodeport service for allure-docker-service api and allure-docker-service ui</li>
  <li>service for allure-docker-service api and allure-docker-service ui</li>
  <li>ingress to item 4</li>
</ol>

## TODO

add more supported parameters  

......

