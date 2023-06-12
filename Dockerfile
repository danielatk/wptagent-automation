FROM golang:1.18 AS builder
WORKDIR /go/src
RUN git clone https://github.com/m-lab/ndt7-client-go
WORKDIR /go/src/ndt7-client-go/cmd/ndt7-client
RUN go mod tidy && go build .

FROM python:3.9.13
ENV QUEUE="default"
WORKDIR /app
RUN apt-get update -y && apt-get install -y traceroute chromium-driver
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs
COPY --from=builder /go/src/ndt7-client-go/cmd/ndt7-client/ndt7-client /usr/local/bin/ndt7-client
ENV DOCKER_VERSION='19.03.8'
RUN set -ex \
    && DOCKER_FILENAME=https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz \
    && curl -L ${DOCKER_FILENAME} | tar -C /usr/bin/ -xzf - --strip-components 1 docker/docker
COPY . /app
RUN pip install -r data_gathering/requirements.txt
CMD ["sh", "-c", "celery -A data_gathering worker -Q data_gathering.${QUEUE} -n ${QUEUE} -l info"]

