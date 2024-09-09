#!/bin/bash
echo "Changing to AP Mode"

systemctl disable hostapd #Enables hostapd

#Change out dhcpcd.conf
mv /etc/dhcpcd.conf /etc/dhcpcd.conf.adhoc
mv /etc/dhcpcd.conf.leaf /etc/dhcpcd.conf

echo "Restart Now"