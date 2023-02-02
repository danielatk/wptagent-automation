#!/bin/sh

echo "Cloning into wptagent-automation repository"

git clone https://github.com/danielatk/wptagent-automation /home/pi/wptagent-automation

set -eu
: ${WPT_SERVER:=''}
: ${WPT_AGENT_KEY:=''}
: ${COLLECTION_SERVER:=''}
: ${COLLECTION_SERVER_USER:=''}
: ${COLLECTION_SERVER_PASSWORD:=''}
: ${COLLECTION_SERVER_SSH_PORT:=''}
: ${COLLECTION_SERVER_NODE_PORT:=''}

while [[ $WPT_SERVER == '' ]]; do
    read -p "WebPageTest server (i.e. www.webpagetest.org): " WPT_SERVER
done
while [[ $WPT_AGENT_KEY == '' ]]; do
    read -p "WebPageTest agent location key (used to communicate with WebPageTest server): " WPT_AGENT_KEY
done
while [[ $COLLECTION_SERVER == '' ]]; do
    read -p "Data collection server (i.e. www.mycollectionserver.com): " COLLECTION_SERVER
done
while [[ $COLLECTION_SERVER_USER == '' ]]; do
    read -p "Data collection server user: " COLLECTION_SERVER_USER
done
while [[ $COLLECTION_SERVER_PASSWORD == '' ]]; do
    read -p "Data collection server password: " COLLECTION_SERVER_PASSWORD
done
while [[ $COLLECTION_SERVER_SSH_PORT == '' ]]; do
    read -p "Data collection server SSH port: " COLLECTION_SERVER_SSH_PORT
done
while [[ $COLLECTION_SERVER_NODE_PORT == '' ]]; do
    read -p "Data collection server node port: " COLLECTION_SERVER_NODE_PORT
done

echo $WPT_SERVER > /home/pi/wptagent-automation/wptserver_url
echo $WPT_AGENT_KEY > /home/pi/wptagent-automation/wptagent_key
echo $COLLECTION_SERVER > /home/pi/wptagent-automation/collection_server_url
echo $COLLECTION_SERVER_USER > /home/pi/wptagent-automation/collection_server_user
echo $COLLECTION_SERVER_PASSWORD > /home/pi/wptagent-automation/collection_server_password
echo $COLLECTION_SERVER_SSH_PORT > /home/pi/wptagent-automation/collection_server_ssh_port
echo $COLLECTION_SERVER_NODE_PORT > /home/pi/wptagent-automation/collection_server_node_port

echo "Saving WebPageTest agent MAC address, which will be it's collection ID."

# saves mac address to /home/pi/wptagent-automation/mac
bash /home/pi/wptagent-automation/scripts/save_mac.sh
mac=$(cat /home/pi/wptagent-automation/mac)
sed -i "s/00:00:00:00:00:00/$mac/" /home/pi/wptagent-automation/scripts/debian.sh

echo "Installing WPTagent."

# install wptagent
bash /home/pi/wptagent-automation/scripts/debian.sh