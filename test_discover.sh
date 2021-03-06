HOST_IP=$(hostname --all-ip-addresses | awk '{print $1}')
ETCD_HOST=$HOST_IP:4001

docker run -it  --name discover --rm   \
-e ETCD_HOST=$ETCD_HOST -e HOST_IP=$HOST_IP  \
-v /var/docker_images/docker-discover:/code \
-v /var/run:/var/run docker-discover /bin/bash

python discover.py
