#!/bin/bash

echo postgres | sudo -S -u postgres psql -d lucas -f /home/nikita/Projects/GAT/sql/refresh_sessions.sql
