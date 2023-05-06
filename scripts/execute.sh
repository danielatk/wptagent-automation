#!/bin/bash

setupFilePath="/home/pi/wptagent-automation/scripts/setup_navigation.py"
togglePuppeteerFilePath="/home/pi/wptagent-automation/scripts/toggle_puppeteer.py"
puppeteerFilePath="/home/pi/wptagent-automation/scripts/puppeteer/puppeteer_navigation/navigation_puppeteer.js"
webdriverFilePath="/home/pi/wptagent-automation/scripts/webdriver/navigation_webdriver.py"
ndtFilePath="/home/pi/wptagent-automation/scripts/ndt/measure_ndt.sh"
ongoingFilePath="/home/pi/wptagent-automation/ongoing"
wptOngoingFilePath="/home/pi/wptagent-automation/wpt_ongoing"
schedulerFilePath="/home/pi/wptagent-automation/scripts/schedule.sh"
logFile="/home/pi/wptagent-automation/log"
macFile="/home/pi/wptagent-automation/mac"
statusFile="/home/pi/wptagent-automation/status"
statusControlScript="/home/pi/wptagent-automation/scripts/status/status_control.sh"

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

# this checks if wpt test has been started via wpt server
bash $statusControlScript

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

echo "$(date +%s) | execute -> setup time" >> $logFile

# setup webdriver and puppeteer tests
args="$(python3 $setupFilePath 2>> $logFile)"

# traceroute to url
url=$(echo $args | cut -d' ' -f1)
traceroute_file_path="./$(cat /home/pi/wptagent-automation/mac)_$(date +%s)_${url}_traceroute"
traceroute -4 $url > "$traceroute_file_path"4
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort "$traceroute_file_path"4 $collectionServerUser@$collectionServerUrl:~/wptagent-control/other_data/
rm "$traceroute_file_path"4

# Webdriver test
python3 $togglePuppeteerFilePath "False" 2>> $logFile

echo "webdriver ${args}" > $statusFile
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $statusFile $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile) >/dev/null 2>&1

echo "$(date +%s) | execute WEBDRIVER -> navigation time ($args)" >> $logFile
python3 $webdriverFilePath $args 2>> $logFile

echo "-------------------" >> $logFile

# puppeteer test
python3 $togglePuppeteerFilePath "True" 2>> $logFile

echo "puppeteer ${args}" > $statusFile
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $statusFile $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile) >/dev/null 2>&1

echo "$(date +%s) | execute PUPPETEER -> navigation time ($args)" >> $logFile
node $puppeteerFilePath $args 2>> $logFile

echo "-------------------" >> $logFile

# ndt test
echo "ndt" > $statusFile
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $statusFile $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile) >/dev/null 2>&1

echo "$(date +%s) | execute NDT -> measuring time" >> $logFile
/bin/bash $measureFilePath 2>> $logFile

echo "-------------------" >> $logFile

echo "0" > $ongoingFilePath

scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ongoingFilePath $collectionServerUser@$collectionServerUrl:~/wptagent-control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1