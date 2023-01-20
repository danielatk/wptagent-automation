#!/bin/sh

git clone https://github.com/danielatk/wptagent-automation ~/wptagent-automation

# saves mac address to ~/wptagent-automation/mac
bash ~/wptagent-automation/scripts/save_mac.sh

# install wptagent
sed -i 's/00:00:00:00:00:00/$(cat ~/wptagent-automation/mac)/' ~/wptagent-automation/scripts/debian.sh
bash ~/wptagent-automation/scripts/debian.sh