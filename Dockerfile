# syntax=docker/dockerfile:1
FROM ubuntu:20.04
WORKDIR /email_routine
RUN  apt update
RUN  apt -y install python3-pip
COPY . .
RUN pip3 install --upgrade certifi
RUN pip3 install -r requirements
