#!/bin/bash

logFile="~/wptagent-automation/log_ndt"
sampleUfFile="~/wptagent-automation/scripts/ndt/sample_from_uf_list.py"

uf="$(python3 $sampleUfFile)"
dateStr="$(date +%s)"
ndt_file_path="~/wptagent-automation/ndt_data/$(cat ~/wptagent-automation/mac)_${dateStr}_${uf}_ndt.json"
traceroute_file_path="~/wptagent-automation/ndt_data/$(cat ~/wptagent-automation/mac)_${dateStr}_${uf}_traceroute"
~/wptagent-automation/scripts/ndt/ndt7-client -server $uf.medidor.rnp.br:4443 -no-verify -scheme wss -format=json > $ndt_file_path
traceroute $uf.medidor.rnp.br > $traceroute_file_path
echo "measure NDT -> test completed successfully" >> $logFile
scp -o StrictHostKeyChecking=no -P 36022 $ndt_file_path $traceroute_file_path localuser@sueste.land.ufrj.br:/media/storage/st1/raspberry_pi_data/ndt_data/
echo "measure NDT -> test data sent to collection server" >> $logFile
echo "-------------------" >> $logFile
rm $ndt_file_path
rm $traceroute_file_path
