#!/bin/bash

measureFilePath="~/wptagent-automation/scripts/ndt/measure_ndt.sh"
ongoingFilePath="~/wptagent-automation/ongoing"
wptOngoingFilePath="~/wptagent-automation/wpt_ongoing"
schedulerFilePath="~/wptagent-automation/scripts/ndt/schedule_ndt.sh"
logFile="~/wptagent-automation/log_ndt"
macFile="~/wptagent-automation/mac"
statusFile="~/wptagent-automation/status"
statusControlScript="~/wptagent-automation/scripts/status/status_control.sh"

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

echo "ndt" > $statusFile
scp -o StrictHostKeyChecking=no -P 36022 $statusFile localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile) >/dev/null 2>&1
scp -o StrictHostKeyChecking=no -P 36022 $ongoingFilePath localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1

echo "$(date +%s) | execute NDT -> scheduling time" >> $logFile
/bin/bash $schedulerFilePath 2>> $logFile

echo "$(date +%s) | execute NDT -> measuring time" >> $logFile
/bin/bash $measureFilePath 2>> $logFile

echo "-------------------" >> $logFile

echo "0" > $ongoingFilePath

scp -o StrictHostKeyChecking=no -P 36022 $ongoingFilePath localuser@sueste.land.ufrj.br:~/wpt_control/status/$(cat $macFile)_ongoing_client >/dev/null 2>&1
