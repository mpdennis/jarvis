#!/bin/bash
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

###  Give the web server access to the i2c bus  ###
# commands were found at https://github.com/Thebanjodude/PiGauge/blob/master/README.md
sudo adduser www-data i2c
sudo /etc/init.d/apache2 restart
