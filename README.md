# docker-discover
Docker化haproxy实现服务发现

## 镜像特点

- 2015/6/21 继承基础镜像docker-register，自身具备服务注册功能

## 使用方法

- 获取代码并构建

        git clone https://github.com/Dockerlover/docker-discover.git
        cd docker-discover
        docker build -t docker-discover .

- 测试服务注册功能[test_register.sh]

        HOST_IP=$(hostname --all-ip-addresses | awk '{print $1}')
        ETCD_HOST=$HOST_IP:4001
        
        docker run -it  --name discover --rm   \
        --net host -p 127.0.0.1:1936:1936 \
        -e ETCD_HOST=$ETCD_HOST -e HOST_IP=$HOST_IP  \
        -v /var/run:/var/run docker-discover /bin/bash
        
        python register.py

- 测试服务发现功能[test_discover.sh]

        HOST_IP=$(hostname --all-ip-addresses | awk '{print $1}')
        ETCD_HOST=$HOST_IP:4001
        
        docker run -it  --name discover --rm   \
        --net host -p 127.0.0.1:1936:1936 \
        -e ETCD_HOST=$ETCD_HOST -e HOST_IP=$HOST_IP  \
        -v /var/run:/var/run docker-discover /bin/bash
        
        python discover.py


- 运行容器

        HOST_IP=$(hostname --all-ip-addresses | awk '{print $1}')
        ETCD_HOST=$HOST_IP:4001
        
        docker run -it  -d --name discover \
        --net host -p 127.0.0.1:1936:1936 \
        -e ETCD_HOST=$ETCD_HOST -e HOST_IP=$HOST_IP  \
        -v /var/run:/var/run docker-discover




