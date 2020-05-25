FROM python:latest

WORKDIR /agent
COPY . ./agent

RUN pip3 install flask flask-cors pymongo requests

EXPOSE 5000