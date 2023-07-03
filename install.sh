#!/usr/bin/bash

#  curl -fsSL https://raw.githubusercontent.com/carloscdias/wptagent-automation/main/install.sh -o - | bash

BASE_DIR='/home/pi/wptagent-automation'


MAC=$(cat /sys/class/net/*/address | head -1)

if [ -f "$BASE_DIR/collection_server_url" ]; then
    SERVER=$(cat "$BASE_DIR/collection_server_url")
else 
    echo "Broker address: "
    read SERVER
fi

if [ -f "$BASE_DIR/wptserver_url" ]; then
    SERVER_URL=$(cat "$BASE_DIR/wptserver_url")
else 
    echo "WPT Server address: "
    read SERVER_URL
fi

if [ -f "$BASE_DIR/wptagent_key" ]; then
    KEY=$(cat "$BASE_DIR/wptagent_key")
else 
    echo "KEY for $SERVER_URL: "
    read KEY
fi
LOCATION=""
NAME=""
SHAPER=""

# install docker
if ! [ -x "$(command -v docker)" ]; then
    curl -fsSL https://get.docker.com -o - | sudo bash
fi
# create directory
git clone --recurse-submodules https://github.com/carloscdias/wptagent-automation.git ~/data_gathering
cd ~/data_gathering/client
# create .env
touch .env
echo "UID=1000" >> .env
echo "QUEUE=\"mac_${MAC}\"" >> .env
echo "BACKEND=\"rpc://guest:guest@${SERVER}/\"" >> .env
echo "BROKER=\"amqp://guest:guest@${SERVER}/\"" >> .env
echo "SERVER_URL=\"${SERVER_URL}\"" >> .env
echo "LOCATION=\"${LOCATION}\"" >> .env
echo "KEY=\"${KEY}\"" >> .env
echo "NAME=\"${NAME}\"" >> .env
echo "SHAPER=\"${SHAPER}\"" >> .env
# start services
sudo docker compose up -d
echo 'Installation completed. Agent is running.'
