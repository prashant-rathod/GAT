#!/bin/bash

pgrep -f gunicorn | xargs kill -9; nohup gunicorn application:application -b localhost:8000 &
