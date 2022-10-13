FROM ubuntu:22.10

RUN apt-get update && apt-get install -y bash bc coreutils curl dumb-init jq net-tools procps python3 python3-pip python3-dev sysstat telnet vim wget

RUN rm -frv /kasa-collector && mkdir -p /kasa-collector

ADD entrypoint.sh /kasa-collector/entrypoint.sh
ADD kasa_collector.py /kasa-collector/kasa_collector.py
ADD tplink_smartplug.py /kasa-collector/tplink_smartplug.py

WORKDIR /kasa-collector

RUN chmod a+x *.sh
RUN chmod a+x *.py

ENTRYPOINT [ "/kasa-collector/entrypoint.sh" ]
