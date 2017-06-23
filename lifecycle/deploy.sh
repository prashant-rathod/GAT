#!/bin/bash 

echo "CLENING LOCAL PROJECT"

./clean.sh

echo "CLEANING PAST VERSIONS ON REMOTE SERVER"

CLEAN_SCRIPT="
rm -rf ~/Projects/GAT/*;
"

ssh -i "aws-ec2-gat1.pem" ubuntu@ec2-52-38-189-7.us-west-2.compute.amazonaws.com "${CLEAN_SCRIPT}"

echo "COPYING FILES"

scp -ri "aws-ec2-gat1.pem" ./* ubuntu@ec2-52-38-189-7.us-west-2.compute.amazonaws.com:~/Projects/GAT/

echo "FINISHING INSTALLATION"

DEPLOY_SCRIPT="
cd ~/Projects/GAT/;
rm -rf deploy.sh setup.sh;

sudo apt-get update;
sudo apt-get upgrade;
sudo apt-get install build-essential;
sudo apt-get install gfortran;
sudo apt-get install python3;
sudo apt-get install python3-pip
sudo apt-get install libatlas-base-dev;
sudo apt-get install liblapack-dev;
sudo apt-get install libpng-dev;
sudo apt-get install zlib1g-dev;
sudo apt-get install libfreetype6-dev;
sudo apt-get install libgeos-dev;
sudo apt-get install libgeos-c1v5;

sudo pip3 install -r requirements.txt;
sudo pip3 install mod_wsgi-httpd;
sudo pip3 install mod_wsgi;
sudo chmod 777 nltk_downloads;
a2enmod wsgi

sudo apachectl restart;
"

ssh -i "aws-ec2-gat1.pem" ubuntu@ec2-52-38-189-7.us-west-2.compute.amazonaws.com "${DEPLOY_SCRIPT}"

echo "SUCCESSFULLY FINISHED DEPLOYMENT"
