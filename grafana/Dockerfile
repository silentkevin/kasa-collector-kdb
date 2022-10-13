FROM grafana/grafana:9.1.8-ubuntu

RUN whoami

USER root

RUN apt-get update -y && \
    apt-get install -y curl iputils-ping telnet wget

USER grafana
