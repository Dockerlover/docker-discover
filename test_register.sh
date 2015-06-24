git pull
HOST_IP=$(hostname --all-ip-addresses | awk '{print $1}')
ETCD_HOST=$HOST_IP:4001

docker stop discover
docker rm discover

docker run -it --net host --name discover --rm -p 127.0.0.1:1936:1936 \
-e ETCD_HOST=$ETCD_HOST -e HOST_IP=$HOST_IP  \
-v /var/run:/var/run -v /var/docker_images/docker-discover:/code docker-discover /bin/bash
