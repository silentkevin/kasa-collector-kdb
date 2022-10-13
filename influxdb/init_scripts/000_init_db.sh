#!/bin/bash -x

influx --execute 'SHOW DATABASES'
influx --execute 'CREATE DATABASE kasa'
influx --execute 'SHOW DATABASES'
