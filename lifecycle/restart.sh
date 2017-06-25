#!/bin/bash

INSTANCE_URL=ubuntu@ec2-52-38-189-7.us-west-2.compute.amazonaws.com
PEM_NAME="aws-ec2-gat1.pem"

echo "RESTARTING NGINX AND GUNICORN"

SCRIPT="
cd ~/Projects/GAT;
sudo service nginx restart;
nohup gunicorn application:application -b localhost:8000 & ;
"

ssh -i "${PEM_NAME}" "${INSTANCE_URL}" "${SCRIPT}"

echo "RESTART COMPLETE"
