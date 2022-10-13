#!/bin/bash -x

sleep 5

env | sort

whoami
id
python3 --version

sleep 1

python3 ./kasa_collector.py

sleep 99999999
