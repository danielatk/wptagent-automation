#!/bin/bash

updateStatusFile="~/wptagent-automation/scripts/status/update_status.py"
statusFile="~/wptagent-automation/status"
macFile="~/wptagent-automation/mac"
wptOngoingFile="~/wptagent-automation/wpt_ongoing"

scp -o StrictHostKeyChecking=no -P 36022 localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile) ./status_temp >/dev/null 2>&1 
scp -o StrictHostKeyChecking=no -P 36022 localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile)_ongoing $wptOngoingFile >/dev/null 2>&1 

if [[ ! -f ./status_temp ]]; then
	exit
fi

if [[ $(diff ./status_temp $statusFile) ]]; then
	touch ./changing
	cp ./status_temp $statusFile
	python3 $updateStatusFile
	rm ./changing
fi

rm ./status_temp
