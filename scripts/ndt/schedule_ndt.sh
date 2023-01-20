#!/bin/bash

randomGeneratorFile="~/wptagent-automation/scripts/generate_exponential.py"
timestampFile="~/wptagent-automation/timestamp_ndt"
logFile="~/wptagent-automation/log_ndt"

# timestamp in milliseconds
timestamp=$(($(date +%s%N)/1000000))

# interval in milliseconds
# sampling from exponential distribution with 60 minutes mean
interval="$(python3 $randomGeneratorFile 60)"

timestampNext=$(($timestamp + $interval))

echo "$(date +%s) | schedule NDT -> next timestamp $timestampNext" >> $logFile
echo $timestampNext > $timestampFile
