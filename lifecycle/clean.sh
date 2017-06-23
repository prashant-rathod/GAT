#!/bin/bash 

echo "CLEAN:"
echo "REMOVING .pyc FILES"
find .. -name \*.pyc -delete

echo "REMOVING __pycache__ DIRS"
find .. -name __pycache__ -type d -delete

echo "CLEAN SUCCESSFUL"
