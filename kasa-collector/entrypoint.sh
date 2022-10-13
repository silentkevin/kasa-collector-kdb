#!/bin/bash -x

env | sort

which conda
ls -lah /opt/conda
ls -lah /opt/conda/envs

whoami
id
/opt/conda/envs/kasa/bin/python3 --version

/opt/conda/envs/kasa/bin/python3 ./kasa_collector.py

sleep 99999999
