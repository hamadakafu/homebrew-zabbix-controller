#!/usr/bin/env bash

set -ex

docker build -t python-build-bin .
docker run --rm -i -t -d --name zabbixctl_builder python-build-bin sleep 30
docker cp $(docker ps -a --latest -q):/app/dist/call_command zabbixctl
docker stop zabbixctl_builder
mv -f zabbixctl bin/zabbixctl