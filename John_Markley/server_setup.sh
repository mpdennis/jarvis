#!/bin/bash
### Configure the keyboard  ###
sudo dpkg-reconfigure keyboard-configuration

### Enable i2c bus  ###
# commands are based on instructions at https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
sed -i '/blacklist i2c-bcm2708/c\\#blacklist i2c-bcm2708' /etc/modprobe.d/raspi-blacklist.conf # comment out the blacklist for i2c
printf "i2c-bcm2708\ni2c-dev\n" >> /etc/modules # load the modules for i2c



### Test the i2c bus  ###
# i2cdetect -y 0 # Revision 1 - China
# i2cdetect -y 1 # Revision 2 - UK


###  Download the i2c tools  ###
sudo apt-get install i2c-tools python-smbus # commands for command line and commands for python

sudo adduser pi i2c # give pi access to the i2c bus


### Install bonjour  ###
sudo apt-get update
sudo apt-get install libnss-mdns


###  Get access through VNC  ###
sudo apt-get install tightvncserver
# vncserver :1 # to turn on the vnc server


###  Install the Apache with PHP  ### 
# instructions are from http://www.instructables.com/id/Raspberry-Pi-Web-Server/step7/Install-Apache-with-PHP/)

sudo apt-get update # updates the repository locations
sudo apt-get install apache2 php5 libapache2-mod-php5 # install apache & php
sudo groupadd www-data
sudo usermod -g www-data www-data
sudo service apache2 restart
sudo chown -R pi /var/www


###  Install the MySQL and  ###
# instructions are from http://www.instructables.com/id/Raspberry-Pi-Web-Server/step8/Install-MySQL/
sudo apt-get install mysql-server mysql-client php5-mysql

###  Clone the repository to the pi  ###
git clone git://github.com/mpdennis/jarvis


###  Update jarvis  ###
# cd /path/to/folder/containing/jarvis/
# git pull


###  Give the web server access to the i2c bus  ###
# commands were found at https://github.com/Thebanjodude/PiGauge/blob/master/README.md
sudo adduser www-data i2c
sudo /etc/init.d/apache2 restart

echo "please restart your pi"
echo "use 'sudo halt' and disconnect the power after 30 seconds then reconnect"
