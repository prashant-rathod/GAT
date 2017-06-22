#!/bin/bash -v

echo "SETTING UP"

SCRIPT="
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

ssh -i "aws-ec2-gat1.pem" ubuntu@ec2-52-38-189-7.us-west-2.compute.amazonaws.com "${SCRIPT}"

echo "SUCCESSFULLY FINISHED SETUP"
