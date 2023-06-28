#!/bin/bash

ongoingFilePath="/home/pi/wptagent-automation/ongoing"
wptOngoingFilePath="/home/pi/wptagent-automation/wpt_ongoing"
logFile="/home/pi/wptagent-automation/log"
macFile="/home/pi/wptagent-automation/mac"
versionFile="/home/pi/wptagent-automation/version"
newVersionFile="/home/pi/wptagent-automation/new_version"
updateScript="/home/pi/wptagent-automation/scripts/update.sh"

collectionServerUrl=$(cat /home/pi/wptagent-automation/collection_server_url)
collectionServerUser=$(cat /home/pi/wptagent-automation/collection_server_user)
collectionServerSshPort=$(cat /home/pi/wptagent-automation/collection_server_ssh_port)

# Set maximum number of iterations to wait for
max_iterations=18  # 18 * 10 seconds = 3 minutes

# Initialize iteration counter
iteration=0

while [ $iteration -lt $max_iterations ]; do
    # Check if there's a local ongoing test
    if [ -f $ongoingFilePath ]; then
        ongoing=$(cat $ongoingFilePath)
    else
        ongoing="0"
    fi

    if [ "$ongoing" = "1" ]; then
        # Wait for 10 seconds before next iteration
        sleep 10
        iteration=$((iteration + 1))
        continue
    fi

    if [ -f $wptOngoingFilePath ]; then
        wptOngoing=$(cat $wptOngoingFilePath)
    else
        wptOngoing="0"
    fi

    if [ "$wptOngoing" = "1" ]; then
        # Wait for 10 seconds before next iteration
        sleep 10
        iteration=$((iteration + 1))
        continue
    fi
    break
done

[ "$ongoing" = "1" ] && echo "$(date +%s) | check update -> ongoing local experiment" >> $logFile && echo "-------------------" >> $logFile && exit
[ "$wptOngoing" = "1" ] && echo "$(date +%s) | check update -> ongoing wpt experiment" >> $logFile && echo "-------------------" >> $logFile && exit

echo "1" > $ongoingFilePath
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ongoingFilePath $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1

scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $collectionServerUser@$collectionServerUrl:~/wptagent-control/update/version $newVersionFile >/dev/null 2>&1

if cmp -s $newVersionFile $versionFile; then
    # there is no new version
    echo "0" > $ongoingFilePath
    scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ongoingFilePath $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1
    echo "$(date +%s) | check update -> no new version" >> $logFile
    echo "-------------------" >> $logFile
    exit
fi

# there is a new version!
echo "$(date +%s) | check update -> new version: $(cat $newVersionFile)" >> $logFile

scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $collectionServerUser@$collectionServerUrl:~/wptagent-control/update/update.sh $updateScript >/dev/null 2>&1

bash $updateScript
rm $updateScript

cp $newVersionFile $versionFile
rm $newVersionFile

echo "0" > $ongoingFilePath
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ongoingFilePath $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1
