FROM python:3.8-alpine

RUN apk update && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev bash

WORKDIR /opt/app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000