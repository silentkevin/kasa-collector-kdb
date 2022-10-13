#!/bin/bash -x

export INFLUX_COMMAND='influx -username if_user -password if_password'

$INFLUX_COMMAND -execute 'SHOW DATABASES'
$INFLUX_COMMAND -execute 'CREATE DATABASE _internal'
$INFLUX_COMMAND -execute 'CREATE DATABASE kasa'
$INFLUX_COMMAND -execute 'SHOW DATABASES'
