FROM python:3.7-alpine

COPY . /app
WORKDIR /app

RUN apk add --no-cache bash
RUN pip install -r requirements.txt
RUN pip install -r requirements-test.txt