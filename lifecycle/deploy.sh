#!/bin/bash 

INSTANCE_URL=ubuntu@ec2-52-37-61-214.us-west-2.compute.amazonaws.com
PEM_NAME="aws-ec2-gat1.pem"

echo "CLENING LOCAL PROJECT"

./clean.sh

echo "CLEANING PAST VERSIONS ON REMOTE SERVER"

CLEAN_SCRIPT="
sudo rm -rf ~/Projects/GAT/*;
"

ssh -i "${PEM_NAME}" "${INSTANCE_URL}" "${CLEAN_SCRIPT}"

echo "COPYING FILES"

scp -ri "${PEM_NAME}" ../* "${INSTANCE_URL}":~/Projects/GAT/

echo "FINISHING INSTALLATION"

DEPLOY_SCRIPT="
cd ~/Projects/GAT/;
rm -rf lifecycle;

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

sudo chmod 777 nltk_downloads;
sudo pip3 install gunicorn;

sudo service nginx restart;
"

ssh -i "${PEM_NAME}" "${INSTANCE_URL}" "${DEPLOY_SCRIPT}"

echo "FINISHED DEPLOYMENT"
