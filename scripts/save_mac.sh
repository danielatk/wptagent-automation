#!/bin/sh

mac=$(ifconfig | grep ether)
mac=${mac%%  txqueuelen*}
mac=${mac#*ether }
mac=${mac//:/}
echo $mac > /home/pi/Documents/mac
