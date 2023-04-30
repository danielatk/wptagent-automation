#!/bin/bash

setupFilePath="/home/pi/wptagent-automation/scripts/setup_navigation.py"
navigationFilePath="/home/pi/wptagent-automation/scripts/webdriver/navigation_webdriver.py"
ongoingFilePath="/home/pi/wptagent-automation/ongoing"
wptOngoingFilePath="/home/pi/wptagent-automation/wpt_ongoing"
schedulerFilePath="/home/pi/wptagent-automation/scripts/webdriver/schedule_webdriver.sh"
logFile="/home/pi/wptagent-automation/log_webdriver"
macFile="/home/pi/wptagent-automation/mac"
statusFile="/home/pi/wptagent-automation/status"
statusControlScript="/home/pi/wptagent-automation/scripts/status/status_control.sh"

if [ -f $ongoingFilePath ]; then
        ongoing=$(cat $ongoingFilePath)
else
        ongoing="0"
fi

[ "$ongoing" = "1" ] && echo "$(date +%s) | execute WEBDRIVER -> ongoing experiment" && echo "-------------------" >> $logFile && exit

# this checks if wpt test has been started via wpt server
bash $statusControlScript

if [ -f $wptOngoingFilePath ]; then
        wptOngoing=$(cat $wptOngoingFilePath)
else
        wptOngoing="0"
fi

[ "$wptOngoing" = "1" ] && echo "$(date +%s) | execute NDT -> ongoing wpt experiment" >> $logFile && echo "-------------------" >> $logFile && exit

echo "1" > $ongoingFilePath

echo "$(date +%s) | execute WEBDRIVER -> scheduling time" >> $logFile
/bin/bash $schedulerFilePath 2>> $logFile

# run dummy Xserver in background
export DISPLAY=:2
Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile /dev/null -config /home/pi/wptagent-automation/xorg.conf :2 &

echo "$(date +%s) | execute WEBDRIVER -> setup time" >> $logFile
args="$(python3 $setupFilePath False 2>> $logFile)"

collectionServerUrl=$(cat /home/pi/wptagent-automation/collection_server_url)
collectionServerUser=$(cat /home/pi/wptagent-automation/collection_server_user)
collectionServerSshPort=$(cat /home/pi/wptagent-automation/collection_server_ssh_port)

echo $args > ./tmp
statusArgs=$(sed 's/[^ ]* //' ./tmp)
rm ./tmp
echo "$(date +%s) | webdriver $statusArgs" > $statusFile
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $statusFile $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile) >/dev/null 2>&1
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ongoingFilePath $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1

echo "$(date +%s) | execute WEBDRIVER -> navigation time ($args)" >> $logFile
python3 $navigationFilePath $args 2>> $logFile

echo "-------------------" >> $logFile

echo "0" > $ongoingFilePath

scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ongoingFilePath $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1
