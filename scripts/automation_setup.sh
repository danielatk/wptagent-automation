#!/bin/bash

echo "Setting up custom ATF-chrome-plugin"

# setup of custom ATF-chrome-plugin
git clone https://github.com/danielatk/ATF-chrome-plugin /home/pi/wptagent-automation/extensions/ATF-chrome-plugin

echo "Setting up custom WPTagent files"

# using custom files
python3 /home/pi/wptagent-automation/scripts/setup_webpagetest_files.py

echo "Installing and setting up golang"

# install go
sudo rm -rf /usr/bin/go

LINUX_ARCH=$(uname -m)
if [ $LINUX_ARCH = aarch64 ]; then
    GO_SOURCE='go1.19.linux-arm64.tar.gz'
else
    GO_SOURCE='go1.19.linux-armv6l.tar.gz'
fi

sudo wget https://go.dev/dl/$GO_SOURCE
sudo tar -C /usr/local -xzf $GO_SOURCE
sudo rm $GO_SOURCE

echo "PATH=\$PATH:/usr/local/go/bin" >> ~/.profile
echo "GOPATH=\$HOME/go" >> ~/.profile

source ~/.profile

cd /home/pi/wptagent-automation/
mkdir ndt_data

echo "Setting up NDT client"

# build ndt client
git clone https://github.com/m-lab/ndt7-client-go
cd ndt7-client-go/cmd/ndt7-client
go mod tidy
go build .
cp ndt7-client ../../../scripts/ndt/

echo "Installing chromedriver and necessary python packages"

# install webdriver and other python packages
sudo apt install -y chromium-chromedriver
pip3 install pandas

echo "Setting up puppeteer"

# configure puppeteer
cd /home/pi/wptagent-automation/scripts/puppeteer/puppeteer_navigation
sudo npm install puppeteer@17.0.0 puppeteer-core@1.20.0 puppeteer-extra@3.3.4 puppeteer-extra-plugin-adblocker@2.13.5 chromium@3.0.3

collectionServerUrl=$(cat /home/pi/wptagent-automation/collection_server_url)
collectionServerUser=$(cat /home/pi/wptagent-automation/collection_server_user)
collectionServerSshPort=$(cat /home/pi/wptagent-automation/collection_server_ssh_port)

echo "Setting up SSH"

# configure ssh
sudo apt install -y sshpass
ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""
sshpass -f /home/pi/wptagent-automation/collection_server_password ssh-copy-id -i ~/.ssh/id_rsa -p $collectionServerSshPort $collectionServerUser@$collectionServerUrl
sudo systemctl enable ssh
sudo systemctl start ssh

echo "Setting up cron jobs"

# adding experiment scripts to crontab
crontab -l > mycron
echo "@reboot /home/pi/wptagent-automation/scripts/status/status_control_loop.sh" >> mycron
echo "@reboot rm /home/pi/wptagent-automation/ongoing" >> mycron
echo "* * * * * sh /home/pi/wptagent-automation/scripts/ndt/check_ndt.sh" >> mycron
echo "* * * * * sh /home/pi/wptagent-automation/scripts/puppeteer/check_puppeteer.sh" >> mycron
echo "* * * * * sh /home/pi/wptagent-automation/scripts/webdriver/check_webdriver.sh" >> mycron
crontab mycron
rm mycron

