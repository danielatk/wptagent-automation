#!/bin/sh

# saves mac address to ~/wptagent-automation/mac
bash ~/wptagent-automation/scripts/save_mac.sh

# install wptagent
# sed -i 's/00:00:00:00:00:00/$(cat ~/wptagent-automation/mac)/' ~/wptagent-automation/scripts/debian.sh
# bash ~/wptagent-automation/scripts/debian.sh

# using custom files
python3 ~/wptagent-automation/scripts/setup_webpagetest_files.py

# install go
sudo rm -rf /usr/bin/go
sudo wget https://go.dev/dl/go1.19.linux-armv6l.tar.gz
sudo tar -C /usr/local -xzf go1.19.linux-armv6l.tar.gz
sudo rm go1.19.linux-armv6l.tar.gz

echo "PATH=\$PATH:/usr/local/go/bin" >> ~/.profile
echo "GOPATH=\$HOME/go" >> ~/.profile

source ~/.profile

cd ~/wptagent-automation/

# build ndt client
git clone https://github.com/m-lab/ndt7-client-go
cd ndt7-client-go/cmd/ndt7-client
go mod tidy
go build .
cp ndt7-client ../../../scripts/ndt/

# install webdriver and other python packages
sudo apt install -y chromium-chromedriver
pip3 install pandas

# configure puppeteer
cd ~/wptagent-automation/scripts/puppeteer/puppeteer_navigation
sudo npm install puppeteer@17.0.0 puppeteer-core@1.20.0 puppeteer-extra@3.3.4 puppeteer-extra-plugin-adblocker@2.13.5 chromium@3.0.3

# configure ssh
sudo apt install -y sshpass
ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""
sshpass -f ~/wptagent-automation/sueste_password ssh-copy-id -i ~/.ssh/id_rsa -p 36022 localuser@sueste.land.ufrj.br
sudo systemctl enable ssh
sudo systemctl start ssh

# adding experiment scripts to crontab
crontab -l > mycron
echo "@reboot ~/wptagent-automation/scripts/status/status_control_loop.sh"
echo "* * * * * sh ~/wptagent-automation/scripts/ndt/check_ndt.sh" >> mycron
echo "* * * * * sh ~/wptagent-automation/scripts/puppeteer/check_puppeteer.sh" >> mycron
echo "* * * * * sh ~/wptagent-automation/scripts/webdriver/check_webdriver.sh" >> mycron
crontab mycron
rm mycron

