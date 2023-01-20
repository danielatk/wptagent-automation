#!/bin/bash

while true; do
	if [[ ! -f ./changing ]]; then
        	bash ./status_control.sh
	fi
	sleep 10
done
