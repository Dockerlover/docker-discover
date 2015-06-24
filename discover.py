from docker import Client
import etcd
import time
import os
from jinja2 import Environment, PackageLoader

POLL_TIMEOUT=60
ETCD_HOST = os.environ["ETCD_HOST"]
HOST_IP = os.environ["HOST_IP"]
DOCKER_HOST = os.environ["DOCKER_HOST"]
DOMAIN_NAME = os.environ["DOMAIN_NAME"]
env = Environment(loader=PackageLoader('haproxy', 'templates'))

def get_etcd_addr():
  etcd_host = os.environ["ETCD_HOST"]
  
  port = 4001
  host = etcd_host

  if ":" in etcd_host:
    host, port = etcd_host.split(":")
  
  return host,port

def reload_haproxy():
  ret = call(["./reload_haproxy.sh"])
  if ret != 0:
    print "reloading haproxy returned: ", ret
  else:
    print "reload haproxy failed!"
  return ret

def write_template(proxy_services):
  template = env.get_template('haproxy.cfg.tmpl')
  with open("/etc/haproxy.cfg", "w") as f:
    f.write(template.render(services=proxy_services))
  return proxy_services


def get_services():

  host, port = get_etcd_addr()
  client = etcd.Client(host=host, port=int(port))
  services = client.read('/services')
  proxy_services = []
  for service in services:
    service_key = service.get("Key",None)
    service_value = service.get("Value",None)
    if(service_key and service_value):
      print 'Error:service not found'
      continue
    service_keys = service_key[1:].split("/")
    service_values = service_value[1:].split("/")
    if(len(service_keys)==4 and len(service_value)>0):
      sub_domain = service_keys[2]+"."+service_keys[1]+"."+DOMAIN_NAME
      host_name = service_keys[3][0:12]
      for port in service_values:
        port_values = service_values.split(":")
        bind_port = port_values[3]
        host_port = port_values[1]+":"+port_values[2]
        
        # write template
        proxy_services.append({"sub_domain":sub_domain,"bind_port":bind_port,"host_name":host_name,"host_port":host_port})
  
  write_template(proxy_services)
  return proxy_services

if __name__ == "__main__":
    while True:
        try:
            services = get_services()
            
            if services:
                print "services had got. "
                write_template(services)
                reload_haproxy()
                time.sleep(POLL_TIMEOUT)
                continue

        except Exception, e:
            print "Error:", e

        time.sleep(POLL_TIMEOUT)
