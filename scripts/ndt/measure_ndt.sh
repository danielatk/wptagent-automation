#!/bin/bash

logFile="/home/pi/wptagent-automation/log_ndt"
sampleUfFile="/home/pi/wptagent-automation/scripts/ndt/sample_from_uf_list.py"
getServerFQDNFile="/home/pi/wptagent-automation/scripts/ndt/get_server_fqdn.py"

collectionServerUrl=$(cat /home/pi/wptagent-automation/collection_server_url)
collectionServerUser=$(cat /home/pi/wptagent-automation/collection_server_user)
collectionServerSshPort=$(cat /home/pi/wptagent-automation/collection_server_ssh_port)

uf="$(python3 $sampleUfFile)"
dateStr="$(date +%s)"
ndt_file_path="/home/pi/wptagent-automation/ndt_data/$(cat /home/pi/wptagent-automation/mac)_${dateStr}_${uf}_ndt.json"
traceroute_file_path="/home/pi/wptagent-automation/ndt_data/$(cat /home/pi/wptagent-automation/mac)_${dateStr}_${uf}_traceroute"
IPV6_FAILURE=false
if [ "$uf" == "mlab" ]; then
    /home/pi/wptagent-automation/scripts/ndt/ndt7-client -no-verify -scheme wss -format=json > $ndt_file_path
    server_fqdn="$(python3 $getServerFQDNFile $ndt_file_path)"
    traceroute -4 $server_fqdn > "$traceroute_file_path"4
    traceroute -6 $server_fqdn > "$traceroute_file_path"6 || IPV6_FAILURE=true
else
    /home/pi/wptagent-automation/scripts/ndt/ndt7-client -server $uf.medidor.rnp.br:4443 -no-verify -scheme wss -format=json > $ndt_file_path
    traceroute -4 $uf.medidor.rnp.br > "$traceroute_file_path"4
    traceroute -6 $uf.medidor.rnp.br > "$traceroute_file_path"6 || IPV6_FAILURE=true
fi
echo "measure NDT -> test completed successfully" >> $logFile
if [ IPV6_FAILURE = false ]; then
    scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ndt_file_path "$traceroute_file_path"4 "$traceroute_file_path"6 $collectionServerUser@$collectionServerUrl:~/wptagent-control/ndt_data/
else
    scp -o StrictHostKeyChecking=no -P $collectionServerSshPort $ndt_file_path "$traceroute_file_path"4 $collectionServerUser@$collectionServerUrl:~/wptagent-control/ndt_data/
    echo "measure NDT -> IPv6 failure, traceroute6 not sent to collection server" >> $logFile
fi
echo "measure NDT -> test data sent to collection server" >> $logFile
echo "-------------------" >> $logFile
rm $ndt_file_path
rm "$traceroute_file_path"4
rm "$traceroute_file_path"6
