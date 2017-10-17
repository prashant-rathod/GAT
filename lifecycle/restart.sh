#!/bin/bash

pgrep -f gunicorn | xargs kill -9;
PATH=/home/ubuntu/.local/bin/:$PATH
nohup gunicorn application:application -b localhost:8000 --timeout 120 >> gunicorn.log 2>&1 &
