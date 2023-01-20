#!/bin/bash

timestampFile="/home/pi/Documents/timestamp_puppeteer"
executionFilePath="/home/pi/Documents/scripts/puppeteer/execute_puppeteer.sh"
logFile="/home/pi/Documents/log_puppeteer"

# before checking sleep a random ammount of time
# (from 0 to 30 seconds in milliseconds granularity)
# this is to prevent race condition

randomMs=$[ $RANDOM % 30000 + 1 ]
ms_unit=0.001
sleep_time=$(echo "scale=3; $randomMs*$ms_unit" | bc)
sleep $sleep_time

if [ -f $timestampFile ]; then
	tsExecute=$(cat $timestampFile)
	tsNow=$(($(date +%s%N)/1000000))
	if [ $tsNow -gt $tsExecute ]; then
		echo "$(date +%s) | check PUPPETEER -> execution time" >> $logFile
		/bin/bash $executionFilePath 2>> $logFile
	fi
else
	echo "$(date +%s) | check PUPPETEER -> first execution" >> $logFile
	/bin/bash $executionFilePath 2>> $logFile
fi

