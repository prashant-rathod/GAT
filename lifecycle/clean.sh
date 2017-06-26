#!/bin/bash 

echo "CLEAN:"
echo "REMOVING .pyc FILES"
find .. -name \*.pyc -delete

echo "REMOVING __pycache__ DIRS"
find .. -name __pycache__ -type d -delete

echo "REMOVING nltk downloads"
find ../nltk_downloads/ -type d -not -name 'track_me' -print0 -delete

echo "CLEAN SUCCESSFUL"
