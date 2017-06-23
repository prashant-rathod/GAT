#!/bin/bash 

echo "SETTING UP"

SCRIPT='
sudo apt-get update;
sudo apt-get upgrade;
sudo apt-get install apache2;
sudo apt-get install libapache2-mod-wsgi-py3;

cd;
mkdir Projects;
cd Projects;
mkdir GAT;
sudo ln -sT ~/Projects/GAT /var/www/html/GAT;
'

ssh -i "aws-ec2-gat1.pem" ubuntu@ec2-52-38-189-7.us-west-2.compute.amazonaws.com "${SCRIPT}"

echo "COPYING APACHE FILES"

scp -i "aws-ec2-gat1.pem" 000-default.conf ubuntu@ec2-52-38-189-7.us-west-2.compute.amazonaws.com:~

COPY_SCRIPT="
sudo mv 000-default.conf /etc/apache2/sites-enabled/
"

ssh -i "aws-ec2-gat1.pem" ubuntu@ec2-52-38-189-7.us-west-2.compute.amazonaws.com "${COPY_SCRIPT}"

echo "SUCCESSFULLY FINISHED SETUP"
