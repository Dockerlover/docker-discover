# 基础镜像
FROM docker-register
# 维护人员
MAINTAINER  liuhong1.happy@163.com
# 安装相关依赖包
RUN apt-get install -y haproxy && \
  sed -i 's/^ENABLED=.*/ENABLED=1/' /etc/default/haproxy

RUN pip install  Jinja2

# 创建Docker配置文件路径
RUN touch /var/run/docker.sock
ENV DOCKER_HOST unix:///var/run/docker.sock
ENV HOST_IP 127.0.0.1
ENV ETCD_HOST 127.0.0.1:4001
VOLUME ["/var/run","/code"]

# 复制代码
COPY . /code
WORKDIR /code


# 配置supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# 启动supervisord
CMD ["/usr/bin/supervisord"]
