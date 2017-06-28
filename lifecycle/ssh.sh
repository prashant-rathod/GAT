#!/bin/bash

INSTANCE_URL=ubuntu@ec2-52-38-189-7.us-west-2.compute.amazonaws.com
PEM_NAME="aws-ec2-gat1.pem"

ssh -i "${PEM_NAME}" "${INSTANCE_URL}"
