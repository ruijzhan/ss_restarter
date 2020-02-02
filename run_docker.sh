#!/bin/bash
CONTAINER=
SS_HOST=
docker rm -fv vyprSS_restart
docker run --name vyprSS_restart \
       -d \
       -m 64m \
       --restart=always \
       --log-opt max-size=10m \
       -v /etc/localtime:/etc/localtime \
       -v /var/run/docker.sock:/var/run/docker.sock ruijzhan/ss_restarter \
       ss_restarter.py -i 30 -c $CONTAINER -s $SS_HOST 
       
