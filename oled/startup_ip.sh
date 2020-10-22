#!/bin/sh
sudo timedatectl set-ntp off
sudo timedatectl set-ntp on
sudo python3 /home/bbot/projects/pybase/oled/oled_show_ip.py
