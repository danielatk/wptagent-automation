FROM golang:1.18 AS builder
WORKDIR /go/src
RUN git clone https://github.com/m-lab/ndt7-client-go
WORKDIR /go/src/ndt7-client-go/cmd/ndt7-client
RUN go mod tidy && go build .

FROM python:3.9.13
ENV QUEUE="default"
WORKDIR /app
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y traceroute chromium-driver xserver-xorg-video-dummy libleveldb-dev
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs
RUN useradd -ms /bin/bash data_gathering
RUN npm install puppeteer@17.0.0 puppeteer-core@1.20.0 puppeteer-extra@3.3.4 chromium@3.0.3
COPY --from=builder /go/src/ndt7-client-go/cmd/ndt7-client/ndt7-client /usr/local/bin/ndt7-client
COPY . /app
RUN mkdir /data
RUN chown -R data_gathering:data_gathering /app /data
USER data_gathering
ENV PATH="$PATH:/app/bin:/home/data_gathering/.local/bin"
RUN pip install -U -r requirements.txt
CMD ["sh", "-c", "start_container"]
