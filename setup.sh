#!/bin/bash -v

echo "SETTING UP"

SCRIPT="
sudo apt-get update; 
sudo apt-get install apache2; 
sudo apt-get install libapache2-mod-wsgi;
sudo apt-get install python-pip;
sudo pip install flask;

mkdir Projects;
cd Projects;
mkdir GAT;
sudo ln -sT GAT /var/www/html/GAT;

MATCH='fields';
INSERT='
WSGIDaemonProcess GAT threads=5
WSGIScriptAlias / /var/www/html/GAT/GAT.wsgi

<Directory GAT>
    WSGIProcessGroup GAT
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
</Directory>';
FILE='/etc/apache2/sites-enabled/000-default.conf';

sed -i 's/$MATCH/$MATCH\n$INSERT/' $FILE;
"

ssh -i "aws-ec2-gat1.pem" ......  "${SCRIPT}"

echo "SUCCESSFULLY FINISHED SETUP"
