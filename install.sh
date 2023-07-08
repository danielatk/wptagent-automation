#!/usr/bin/bash

#  curl -fsSL https://raw.githubusercontent.com/danielatk/wptagent-automation/alpha/install.sh -o - | bash

BASE_DIR='/home/pi/wptagent-automation'


# MAC=$(cat /sys/class/net/*/address | head -1)

mac=$(ifconfig | grep ether)
mac=${mac%%  txqueuelen*}
mac=${mac#*ether }
MAC=${mac//:/}

set -eu
: ${WPT_SERVER:=''}
: ${WPT_KEY:=''}
: ${BROKER:=''}
: ${COLLECTION_SERVER:=''}
: ${COLLECTION_SERVER_PORT:=''}

if [ -f "$BASE_DIR/broker_url" ]; then
    BROKER=$(cat "$BASE_DIR/broker_url")
fi 
while [[ $BROKER == '' ]]; do
    read -p "Broker address: " BROKER
done

if [ -f "$BASE_DIR/collection_server_url" ]; then
    COLLECTION_SERVER=$(cat "$BASE_DIR/collection_server_url")
fi 
while [[ $COLLECTION_SERVER == '' ]]; do
    read -p "Collection server address: " COLLECTION_SERVER
done

if [ -f "$BASE_DIR/collection_server_port" ]; then
    COLLECTION_SERVER_PORT=$(cat "$BASE_DIR/collection_server_port")
fi 
while [[ $COLLECTION_SERVER_PORT == '' ]]; do
    read -p "Collection server port: " COLLECTION_SERVER_PORT
done

if [ -f "$BASE_DIR/wptserver_url" ]; then
    WPT_SERVER=$(cat "$BASE_DIR/wptserver_url")
fi
while [[ $WPT_SERVER == '' ]]; do
    read -p "WebPageTest server address: " WPT_SERVER
done

if [ -f "$BASE_DIR/wptagent_key" ]; then
    WPT_KEY=$(cat "$BASE_DIR/wptagent_key")
fi
while [[ $WPT_KEY == '' ]]; do
    read -p "WebPageTest agent location key for $WPT_SERVER: " WPT_KEY
done

NAME=""
SHAPER=""

# install docker
if ! [ -x "$(command -v docker)" ]; then
    curl -fsSL https://get.docker.com -o - | sudo bash
fi

# create directory
git clone --recurse-submodules -b alpha https://github.com/danielatk/wptagent-automation.git ~/data_gathering
cd ~/data_gathering/client

# modify plugin
for file in "~/data_gathering/client/resources/extensions/ATF-chrome-plugin"/*; do
    if [ -f "$file" ]; then
        filedata=$(<"$file")

        filedata=${filedata//'00:00:00:00:00:00'/$MAC}
        filedata=${filedata//'0.0.0.0'/$COLLECTION_SERVER}
        filedata=${filedata//'65535'/$COLLECTION_SERVER_PORT}

        echo "$filedata" > "$file"
    fi
done

# create .env
touch .env
echo "UID=1000" >> .env
echo "QUEUE=\"mac_${MAC}\"" >> .env
echo "BACKEND=\"rpc://guest:guest@${BROKER}/\"" >> .env
echo "BROKER=\"amqp://guest:guest@${BROKER}/\"" >> .env
echo "WPT_SERVER=\"${WPT_SERVER}\"" >> .env
echo "LOCATION=\"${MAC}\"" >> .env
echo "WPT_KEY=\"${WPT_KEY}\"" >> .env
echo "NAME=\"${NAME}\"" >> .env
echo "SHAPER=\"${SHAPER}\"" >> .env

# start services
sudo docker compose up -d --build
echo 'Installation completed. Agent is running.'
