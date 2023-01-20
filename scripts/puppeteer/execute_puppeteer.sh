#!/bin/bash

setupFilePath="/home/pi/Documents/scripts/setup_navigation.py"
navigationFilePath="/home/pi/Documents/scripts/puppeteer/puppeteer_navigation/navigation_puppeteer.js"
ongoingFilePath="/home/pi/Documents/ongoing"
wptOngoingFilePath="/home/pi/Documents/wpt_ongoing"
schedulerFilePath="/home/pi/Documents/scripts/puppeteer/schedule_puppeteer.sh"
logFile="/home/pi/Documents/log_puppeteer"
macFile="/home/pi/Documents/mac"
statusFile="/home/pi/Documents/status"
statusControlScript="/home/pi/Documents/scripts/status/status_control.sh"

if [ -f $ongoingFilePath ]; then
        ongoing=$(cat $ongoingFilePath)
else
        ongoing="0"
fi

[ "$ongoing" = "1" ] && echo "$(date +%s) | execute PUPPETEER -> ongoing experiment" && echo "-------------------" >> $logFile && exit

# this checks if wpt test has been started via wpt server
bash $statusControlScript

if [ -f $wptOngoingFilePath ]; then
        wptOngoing=$(cat $wptOngoingFilePath)
else
        wptOngoing="0"
fi

[ "$wptOngoing" = "1" ] && echo "$(date +%s) | execute NDT -> ongoing wpt experiment" >> $logFile && echo "-------------------" >> $logFile && exit

echo "1" > $ongoingFilePath

echo "$(date +%s) | execute PUPPETEER -> scheduling time" >> $logFile
/bin/bash $schedulerFilePath 2>> $logFile

# run dummy Xserver in background
export DISPLAY=:2
Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile /dev/null -config ~/Documents/xorg.conf :2 &

echo "$(date +%s) | execute PUPPETEER -> setup time" >> $logFile
args="$(python3 $setupFilePath True 2>> $logFile)"

echo $args > ./tmp
statusArgs=$(sed 's/[^ ]* //' ./tmp)
rm ./tmp
echo "puppeteer $statusArgs" > $statusFile
scp -o StrictHostKeyChecking=no -P 36022 $statusFile localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile) >/dev/null 2>&1
scp -o StrictHostKeyChecking=no -P 36022 $ongoingFilePath localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1

echo "$(date +%s) | execute PUPPETEER -> navigation time ($args)" >> $logFile
node $navigationFilePath $args 2>> $logFile

echo "-------------------" >> $logFile

echo "0" > $ongoingFilePath

scp -o StrictHostKeyChecking=no -P 36022 $ongoingFilePath localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1
