#!/bin/bash
echo "Changing to AP Mode"

systemctl enable hostapd #Enables hostapd

#Change out dhcpcd.conf
mv /etc/dhcpcd.conf /etc/dhcpcd.conf.leaf
mv /etc/dhcpcd.conf.adhoc /etc/dhcpcd.conf

echo "Restart Now"