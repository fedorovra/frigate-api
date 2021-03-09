#!/usr/bin/env bash

cd /root/frigate-api
/usr/local/miniconda3/envs/frigate-api/bin/python \
                                                  /usr/local/miniconda3/envs/frigate-api/bin/gunicorn \
                                                  --bind 192.168.88.254:1025 \
                                                  --daemon \
                                                  --reload \
                                                  --access-logfile log/access.log \
                                                  --error-logfile log/error.log \
                                                  api.wsgi
