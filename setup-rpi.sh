#!/bin/sh
# setup-rpi.sh

sudo su
pcmanfm --set-wallpaper /home/pi/TacOS/Graphics/TacOS.png
cp /home/pi/TacOS/Data/lxde-autostart.txt /etc/xdg/lxsession/LXDE-pi/autostart
raspi-config
reboot