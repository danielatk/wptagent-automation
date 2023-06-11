FROM golang:1.18 AS builder
WORKDIR /go/src
RUN git clone https://github.com/m-lab/ndt7-client-go
WORKDIR /go/src/ndt7-client-go/cmd/ndt7-client
RUN go mod tidy && go build .

FROM python:3.9.13
ENV QUEUE="default"
WORKDIR /app
COPY . /app
RUN apt-get update -y && apt-get install -y traceroute chromium-driver
COPY --from=builder /go/src/ndt7-client-go/cmd/ndt7-client/ndt7-client /usr/local/bin/ndt7-client
RUN pip install -r data_gathering/requirements.txt
CMD ["sh", "-c", "celery -A data_gathering worker -Q data_gathering.${QUEUE} -n ${QUEUE} -l info"]

