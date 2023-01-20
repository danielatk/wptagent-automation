#!/bin/bash

setupFilePath="~/wptagent-automation/scripts/setup_navigation.py"
navigationFilePath="~/wptagent-automation/scripts/webdriver/navigation_webdriver.py"
ongoingFilePath="~/wptagent-automation/ongoing"
wptOngoingFilePath="~/wptagent-automation/wpt_ongoing"
schedulerFilePath="~/wptagent-automation/scripts/webdriver/schedule_webdriver.sh"
logFile="~/wptagent-automation/log_webdriver"
macFile="~/wptagent-automation/mac"
statusFile="~/wptagent-automation/status"
statusControlScript="~/wptagent-automation/scripts/status/status_control.sh"

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
Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile /dev/null -config ~/Documents/xorg.conf :2 &

echo "$(date +%s) | execute WEBDRIVER -> setup time" >> $logFile
args="$(python3 $setupFilePath False 2>> $logFile)"

echo $args > ./tmp
statusArgs=$(sed 's/[^ ]* //' ./tmp)
rm ./tmp
echo "$(date +%s) | puppeteer $statusArgs" > $statusFile
scp -o StrictHostKeyChecking=no -P 36022 $statusFile localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile) >/dev/null 2>&1
scp -o StrictHostKeyChecking=no -P 36022 $ongoingFilePath localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1

echo "$(date +%s) | execute WEBDRIVER -> navigation time ($args)" >> $logFile
python3 $navigationFilePath $args 2>> $logFile

echo "-------------------" >> $logFile

echo "0" > $ongoingFilePath

scp -o StrictHostKeyChecking=no -P 36022 $ongoingFilePath localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1
