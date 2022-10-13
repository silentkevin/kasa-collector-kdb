FROM continuumio/anaconda3:2022.05

RUN apt-get update && apt-get install -y bash bc coreutils curl dumb-init jq net-tools procps sysstat telnet vim wget

RUN rm -frv /kasa-collector && mkdir -p /kasa-collector

RUN which conda && conda --version
RUN conda update -y -n base -c defaults conda
RUN which conda && conda --version

WORKDIR /kasa-collector

ADD kasa_env.yml /kasa-collector/kasa_env.yml
RUN conda info --envs && \
    conda env create -f kasa_env.yml
RUN conda info --envs && \
    conda env export -n kasa

ADD entrypoint.sh /kasa-collector/entrypoint.sh
ADD kasa_collector.py /kasa-collector/kasa_collector.py

RUN chmod a+x *.sh
RUN chmod a+x *.py

ENTRYPOINT [ "/kasa-collector/entrypoint.sh" ]
