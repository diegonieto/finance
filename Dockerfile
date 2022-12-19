FROM        ubuntu:20.04 AS base

WORKDIR     /tmp/finance

RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends \
        sqlite3 \
        python3 \
        ca-certificates \
        git \
        python3-pip

ARG DEBIAN_FRONTEND=noninteractive

RUN     git clone https://github.com/diegonieto/finance /tmp/finance && \
        pip3 install -r requirements.txt
