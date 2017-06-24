#!/bin/bash

echo "RESTARTING NGINX AND GUNICORN"

SCRIPT="
cd ~/Projects/GAT;
sudo service nginx restart;
nohup gunicorn application:application -b localhost:8000 &;
"

ssh -i "aws-ec2-gat1.pem" ubuntu@ec2-52-38-189-7.us-west-2.compute.amazonaws.com "${SCRIPT}"

echo "RESTART COMPLETE"
