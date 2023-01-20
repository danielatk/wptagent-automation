#!/bin/bash

logFile="~/wptagent-automation/log_ndt"
sampleUfFile="~/wptagent-automation/scripts/ndt/sample_from_uf_list.py"

collectionServerUrl=$(cat ~/wptagent-automation/collection_server_url)
collectionServerUser=$(cat ~/wptagent-automation/collection_server_user)
collectionServerSshPort=$(cat ~/wptagent-automation/collection_server_ssh_port)

uf="$(python3 $sampleUfFile)"
dateStr="$(date +%s)"
ndt_file_path="~/wptagent-automation/ndt_data/$(cat ~/wptagent-automation/mac)_${dateStr}_${uf}_ndt.json"
traceroute_file_path="~/wptagent-automation/ndt_data/$(cat ~/wptagent-automation/mac)_${dateStr}_${uf}_traceroute"
~/wptagent-automation/scripts/ndt/ndt7-client -server $uf.medidor.rnp.br:4443 -no-verify -scheme wss -format=json > $ndt_file_path
traceroute $uf.medidor.rnp.br > $traceroute_file_path
echo "measure NDT -> test completed successfully" >> $logFile
scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ndt_file_path $traceroute_file_path $collectionServerUser@$collectionServerUrl:~/wptagent-control/ndt_data/
echo "measure NDT -> test data sent to collection server" >> $logFile
echo "-------------------" >> $logFile
rm $ndt_file_path
rm $traceroute_file_path
