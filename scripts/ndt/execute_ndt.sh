#!/bin/bash

measureFilePath="/home/pi/wptagent-automation/scripts/ndt/measure_ndt.sh"
ongoingFilePath="/home/pi/wptagent-automation/ongoing"
wptOngoingFilePath="/home/pi/wptagent-automation/wpt_ongoing"
schedulerFilePath="/home/pi/wptagent-automation/scripts/ndt/schedule_ndt.sh"
logFile="/home/pi/wptagent-automation/log_ndt"
macFile="/home/pi/wptagent-automation/mac"
statusFile="/home/pi/wptagent-automation/status"
statusControlScript="/home/pi/wptagent-automation/scripts/status/status_control.sh"

if [ -f $ongoingFilePath ]; then
	ongoing=$(cat $ongoingFilePath)
else
	ongoing="0"
fi

[ "$ongoing" = "1" ] && echo "$(date +%s) | execute NDT -> ongoing experiment" >> $logFile && echo "-------------------" >> $logFile && exit

# this checks if wpt test has been started via wpt server
bash $statusControlScript

if [ -f $wptOngoingFilePath ]; then
        wptOngoing=$(cat $wptOngoingFilePath)
else
        wptOngoing="0"
fi

[ "$wptOngoing" = "1" ] && echo "$(date +%s) | execute NDT -> ongoing wpt experiment" >> $logFile && echo "-------------------" >> $logFile && exit

echo "1" > $ongoingFilePath

collectionServerUrl=$(cat /home/pi/wptagent-automation/collection_server_url)
collectionServerUser=$(cat /home/pi/wptagent-automation/collection_server_user)
collectionServerSshPort=$(cat /home/pi/wptagent-automation/collection_server_ssh_port)

echo "ndt" > $statusFile
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $statusFile $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile) >/dev/null 2>&1
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ongoingFilePath $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1

echo "$(date +%s) | execute NDT -> scheduling time" >> $logFile
/bin/bash $schedulerFilePath 2>> $logFile

echo "$(date +%s) | execute NDT -> measuring time" >> $logFile
/bin/bash $measureFilePath 2>> $logFile

echo "-------------------" >> $logFile

echo "0" > $ongoingFilePath

scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ongoingFilePath $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1
