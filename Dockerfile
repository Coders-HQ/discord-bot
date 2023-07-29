FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
COPY README.md README.md
RUN pip3 install -r requirements.txt

COPY ./micro ./micro
