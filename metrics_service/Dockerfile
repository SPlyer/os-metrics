FROM ubuntu:19.10

RUN apt-get update

RUN apt-get install -y \
    python3 \
    python3-pip

WORKDIR /usr/src/service

COPY . .

RUN pip3 install -r requirements.txt