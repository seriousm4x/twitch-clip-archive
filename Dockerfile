FROM python:3-alpine

RUN apk update && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev bash

WORKDIR /opt/app
COPY . .
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["./run.sh"]
