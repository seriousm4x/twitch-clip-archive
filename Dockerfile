FROM python:3-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/dl-5.alpinelinux.org/g' /etc/apk/repositories &&\
    apk update && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev bash &&\
    adduser -D clipuser

USER clipuser

WORKDIR /opt/app

COPY --chown=clipuser:clipuser . .

ENV PATH="/home/clipuser/.local/bin:${PATH}"

RUN pip install --user -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["./run.sh"]
