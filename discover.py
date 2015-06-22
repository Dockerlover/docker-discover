from docker import Client
import etcd
import time
import os
from jinja2 import Environment, PackageLoader

POLL_TIMEOUT=60
ETCD_HOST = os.environ["ETCD_HOST"]
HOST_IP = os.environ["HOST_IP"]
DOCKER_HOST = os.environ["DOCKER_HOST"]
env = Environment(loader=PackageLoader('haproxy', 'templates'))

def get_etcd_addr():
  etcd_host = os.environ["ETCD_HOST"]
  
  port = 4001
  host = etcd_host

  if ":" in etcd_host:
    host, port = etcd_host.split(":")
  
  return host,port

def get_services():

  host, port = get_etcd_addr()
  client = etcd.Client(host=host, port=int(port))
  
  _services = client.read('/services', recursive = True)
  print "[Info: print services]",_services
  res_services = {}
  for child in _services.children:
    print "[Info: print service child key]",child.key[1:]
    _prefix , container_name = child.key[1:].split("/")
    print "[Info: print container_name]",container_name
    image_name = client.read(child.key+'/image' , recursive = True).value
    container_status = client.read(child.key+'/status' , recursive = True).value
    _ports = client.read(child.key+'/ports' , recursive = True)
    container_ports = []

    for port in _prots.children:
      _prefix , _name_prefix , _port_prefix , ip_port  = port.key[1:].split("/")
      _type = port.value
      ip , port = ip_port.split(":")
      container_ports.append({"type":_type,"ip":ip,"port":port})
      print "[Info: print ip and port]",_type,ip , port
    res_services[container_name] = {
      "name":container_name,
      "image":image_name,
      "status":container_status,
      "ports":container_ports
    }
    
  return res_services


def write_template(services):
  print services

def reload_haproxy():
  print "reload haproxy."
  

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
