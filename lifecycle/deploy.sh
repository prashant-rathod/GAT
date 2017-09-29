#!/bin/bash 

INSTANCE_URL=ubuntu@ec2-52-37-61-214.us-west-2.compute.amazonaws.com
PEM_NAME="aws-ec2-gat1.pem"

echo "CLENING LOCAL PROJECT"

./clean.sh

echo "CLEANING PAST VERSIONS ON REMOTE SERVER"

CLEAN_SCRIPT="
cd ~/Projects/GAT/lifecycle;
./clean.sh;
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

sudo python3 -m spacy download en

sudo service nginx restart;

sudo update-rc.d postgresql enable;
sudo service postgresql start;
sudo chmod 755 lifecycle/refresh_sessions.sh;
mv lifecycle/refresh_sessions.sh /etc/cron.hourly/;

chmod +x lifecycle/restart.sh;
lifecycle/restart.sh
"

ssh -i "${PEM_NAME}" "${INSTANCE_URL}" "${DEPLOY_SCRIPT}"

echo "FINISHED DEPLOYMENT"
