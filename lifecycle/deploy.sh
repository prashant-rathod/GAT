#!/bin/bash 

INSTANCE_URL=ubuntu@ec2-52-88-172-21.us-west-2.compute.amazonaws.com
PEM_NAME="aws-ec2-gat1.pem"

echo "CLENING LOCAL PROJECT"

./clean.sh

echo "CLEANING PAST VERSIONS ON REMOTE SERVER"

CLEAN_SCRIPT="
~/Projects/GAT/lifecycle/clean.sh;
"

ssh -i "${PEM_NAME}" "${INSTANCE_URL}" "${CLEAN_SCRIPT}"

echo "COPYING FILES"
rsync -avz --exclude-from='exclude' -e "ssh -i ${PEM_NAME}" ../ "${INSTANCE_URL}":~/Projects/GAT/

echo "FINISHING INSTALLATION"

DEPLOY_SCRIPT="
cd ~/Projects/GAT/;
sudo add-apt-repository ppa:ubuntugis/ppa;
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
sudo apt-get install gdal-bin;
sudo apt-get install libxslt1-dev python-dev python-shapely python-gdal python-pyproj python-pip;
sudo apt install libgdal-dev;
sudo pip2 install https://github.com/kartograph/kartograph.py/zipball/master -r https://raw.github.com/kartograph/kartograph.py/master/requirements.txt;
sudo pip3 install -r requirements.txt;

sudo chmod 777 nltk_downloads;
sudo pip3 install gunicorn;

sudo python3 -m spacy download en;

cd gat/service/SmartSearch;
wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip;
unzip chromedriver_linux64.zip;
chmod +x chromedriver;

cd ~/Projects/GAT;

sudo service nginx restart;

chmod +x lifecycle/restart.sh;
lifecycle/restart.sh
"

ssh -i "${PEM_NAME}" "${INSTANCE_URL}" "${DEPLOY_SCRIPT}"

echo "FINISHED DEPLOYMENT"
