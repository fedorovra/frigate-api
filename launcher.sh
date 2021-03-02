#!/usr/bin/env bash

cd /root/frigate-api
/usr/local/miniconda3/envs/frigate-api/bin/python /usr/local/miniconda3/envs/frigate-api/bin/gunicorn --bind 192.168.88.254:9000 --daemon --reload api.wsgi
