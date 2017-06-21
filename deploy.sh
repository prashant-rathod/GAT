#!/bin/bash -v

echo "CLEANING PAST VERSIONS"

CLEAN_SCRIPT="
rm -rf ~/Projects/GAT/*;
"

ssh -i "aws-ec2-gat1.pem" ......  "${CLEAN_SCRIPT}"

echo "COPYING FILES"

scp -i "aws-ec2-gat1.pem" ./* ....~/Projects/GAT/

echo "FINISHING INSTALLATION"

DEPLOY_SCRIPT="
cd ~/Projects/GAT/;
rm -rf deploy.sh setup.sh

#TODO: Install manual stuff with apt-get - see old files in .ebextensions

sudp pip install -r requirements.txt

sudo apachectl restart;
"

ssh -i "aws-ec2-gat1.pem" ......  "${DEPLOY_SCRIPT}"

echo "SUCCESSFULLY FINISHED DEPLOYMENT"
