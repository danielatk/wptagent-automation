#!/bin/bash

updateStatusFile="/home/pi/wptagent-automation/scripts/status/update_status.py"
statusFile="/home/pi/wptagent-automation/status"
macFile="/home/pi/wptagent-automation/mac"
wptOngoingFile="/home/pi/wptagent-automation/wpt_ongoing"

collectionServerUrl=$(cat /home/pi/wptagent-automation/collection_server_url)
collectionServerUser=$(cat /home/pi/wptagent-automation/collection_server_user)
collectionServerSshPort=$(cat /home/pi/wptagent-automation/collection_server_ssh_port)

scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile) ./status_temp >/dev/null 2>&1 
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing $wptOngoingFile >/dev/null 2>&1 

if [[ ! -f /home/pi/wptagent-automation/status_temp ]]; then
	exit
fi

if [[ $(diff ./status_temp $statusFile) ]]; then
	touch ./changing
	cp ./status_temp $statusFile
	python3 $updateStatusFile
	# check if there's a new WPT test. If there is must trigger a traceroute test to the URL that will be tested
	tool=$(cat $statusFile | cut -d' ' -f1)
	if [ $tool = "wpt" ]; then
		url=$(cat $statusFile | cut -d' ' -f2)
		if [[ $url == *"watch?v="* ]]; then
			url="www.youtube.com"
		fi
		if [[ $url == "http://"* ]]; then
			url=${url/http:\/\//}
		fi
		if [[ $url == "https://"* ]]; then
			url=${url/http:\/\//}
		fi
		traceroute_file_path="./$(cat /home/pi/wptagent-automation/mac)_$(date +%s)_${url}_traceroute"
		traceroute -4 $url > "$traceroute_file_path"4
		scp -o StrictHostKeyChecking=no -P $collectionServerSshPort "$traceroute_file_path"4 $collectionServerUser@$collectionServerUrl:~/wptagent-control/wpt_data/
		rm "$traceroute_file_path"4
	fi
	rm ./changing
fi

rm /home/pi/wptagent-automation/status_temp
