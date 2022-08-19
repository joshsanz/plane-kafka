FROM confluentinc/ksql-clickstream-demo:5.0.0 AS confluent-base

LABEL version="1.0"
LABEL description="Extending confluentinc/ksql image adding a few more packages"

#ENV http_proxy=
#ENV https_proxy=

RUN apt-get update
RUN apt-get install vim-tiny -y


FROM confluent-base as initialized

ADD ./scripts /scripts
ADD ./raspberry-pi /raspberry-pi
WORKDIR /scripts
# Need setup scripts in same parent PID as confluent start to preserve state
RUN ./setup_all

ENTRYPOINT ["/bin/sh", "-c", "/scripts/run_confluent"]
# I know you are not supposed to do this, it's not very docker-like
# ENTRYPOINT ["tail", "-f", "/dev/null"]

VOLUME ["/scripts", "/raspberry-pi", "/var/lib/zookeeper/data", "/var/lib/zookeeper/log", "/var/lib/kafka/data"]
