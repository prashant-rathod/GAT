#!/bin/bash

INSTANCE_URL=ubuntu@ec2-52-37-61-214.us-west-2.compute.amazonaws.com
PEM_NAME="aws-ec2-gat1.pem"

ssh -i "${PEM_NAME}" "${INSTANCE_URL}"
