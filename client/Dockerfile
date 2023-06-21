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
RUN npm install puppeteer@17.0.0 puppeteer-core@1.20.0 puppeteer-extra@3.3.4 puppeteer-extra-plugin-adblocker@2.13.5 chromium@3.0.3
COPY --from=builder /go/src/ndt7-client-go/cmd/ndt7-client/ndt7-client /usr/local/bin/ndt7-client
COPY . /app
RUN pip install -r requirements.txt
CMD ["sh", "-c", "celery -A data_gathering worker -Q data_gathering.${QUEUE} -n ${QUEUE} -l info"]
