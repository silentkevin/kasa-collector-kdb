#!/bin/bash -x

sleep 5

env | sort

which conda
ls -lah /opt/conda
ls -lah /opt/conda/envs

whoami
id
/opt/conda/envs/kasa/bin/python3 --version

sleep 1

/opt/conda/envs/kasa/bin/python3 ./kasa_collector.py

sleep 99999999
