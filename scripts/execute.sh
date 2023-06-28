#!/bin/bash

setupNavigationFilePath="/home/pi/wptagent-automation/scripts/setup_navigation.py"
setupReproductionFilePath="/home/pi/wptagent-automation/scripts/setup_reproduction.py"
navigationFilePath="/home/pi/wptagent-automation/scripts/puppeteer/puppeteer_navigation/navigation_puppeteer.js"
reproductionFilePath="/home/pi/wptagent-automation/scripts/webdriver/reproduction_webdriver.py"
ndtFilePath="/home/pi/wptagent-automation/scripts/ndt/measure_ndt.sh"
ongoingFilePath="/home/pi/wptagent-automation/ongoing"
wptOngoingFilePath="/home/pi/wptagent-automation/wpt_ongoing"
schedulerFilePath="/home/pi/wptagent-automation/scripts/schedule.sh"
navigationListFilePath="/home/pi/wptagent-automation/navigation_list.csv"
navigationSampleListFilePath="/home/pi/wptagent-automation/navigation_sample_list"
logFile="/home/pi/wptagent-automation/log"
macFile="/home/pi/wptagent-automation/mac"

collectionServerUrl=$(cat /home/pi/wptagent-automation/collection_server_url)
collectionServerUser=$(cat /home/pi/wptagent-automation/collection_server_user)
collectionServerSshPort=$(cat /home/pi/wptagent-automation/collection_server_ssh_port)

# check if there's a local ongoing test

if [ -f $ongoingFilePath ]; then
        ongoing=$(cat $ongoingFilePath)
else
        ongoing="0"
fi

[ "$ongoing" = "1" ] && echo "$(date +%s) | execute -> previous experiment didn't finish" && echo "-------------------" >> $logFile && exit

if [ -f $wptOngoingFilePath ]; then
        wptOngoing=$(cat $wptOngoingFilePath)
else
        wptOngoing="0"
fi

[ "$wptOngoing" = "1" ] && echo "$(date +%s) | execute -> ongoing wpt experiment" >> $logFile && echo "-------------------" >> $logFile && exit

echo "1" > $ongoingFilePath

scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ongoingFilePath $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1

echo "$(date +%s) | execute -> scheduling time" >> $logFile
/bin/bash $schedulerFilePath 2>> $logFile

# run dummy Xserver in background
export DISPLAY=:2
if [ ! -f /tmp/.X2-lock ]; then
        Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile /dev/null -config /home/pi/wptagent-automation/xorg.conf :2 &
fi

echo "$(date +%s) | execute NDT -> measuring time" >> $logFile
/bin/bash $ndtFilePath 2>> $logFile

echo "-------------------" >> $logFile

# navigate all the pages

while IFS= read -r line; do
    args="$(python3 $setupNavigationFilePath)"

    echo "$(date +%s) | execute PUPPETEER -> navigation time ($args)" >> $logFile

    node $navigationFilePath $args 2>> $logFile

    echo "-------------------" >> $logFile
done < $navigationListFilePath

rm $navigationSampleListFilePath

echo "-------------------" >> $logFile

args="$(python3 $setupReproductionFilePath)"

echo "$(date +%s) | execute WEBDRIVER -> reproduction time ($args)" >> $logFile

python3 $reproductionFilePath $args 2>> $logFile

echo "-------------------" >> $logFile

echo "0" > $ongoingFilePath

scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ongoingFilePath $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1
