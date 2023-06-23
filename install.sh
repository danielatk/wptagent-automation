#!/usr/bin/bash

MAC=$(cat /sys/class/net/*/address | head -1)
# install docker
curl -fsSL https://get.docker.com -o - | sudo bash
# create directory
git clone --recurse-submodules https://github.com/carloscdias/wptagent-automation.git ~/data_gathering
