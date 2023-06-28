#!/bin/bash

macFile="/home/pi/wptagent-automation/mac"
wptOngoingFile="/home/pi/wptagent-automation/wpt_ongoing"

collectionServerUrl=$(cat /home/pi/wptagent-automation/collection_server_url)
collectionServerUser=$(cat /home/pi/wptagent-automation/collection_server_user)
collectionServerSshPort=$(cat /home/pi/wptagent-automation/collection_server_ssh_port)


while true; do
	scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing $wptOngoingFile >/dev/null 2>&1 
	sleep 10
done