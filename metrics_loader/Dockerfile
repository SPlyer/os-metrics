FROM ubuntu:19.10

RUN apt-get update

RUN apt-get install -y \
    python3 \
    python3-pip \
    git

WORKDIR /usr/src/metrics_loader

COPY metrics_loader/requirements.txt .

RUN pip3 install -r requirements.txt
