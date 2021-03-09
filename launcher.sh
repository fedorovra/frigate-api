#!/usr/bin/env bash

cd /root/frigate-api
/usr/local/miniconda3/envs/frigate-api/bin/python \
                                                  /usr/local/miniconda3/envs/frigate-api/bin/gunicorn \
                                                  --config settings.py \
                                                  --access-logfile log/access.log \
                                                  --error-logfile log/error.log \
                                                  api.wsgi
