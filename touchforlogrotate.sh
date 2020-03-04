#!/bin/bash

DIR=`echo $(cd "$(dirname "$0")"; pwd)`
LOGDIR="${DIR}/logs"

sourcelogpath="${DIR}/uwsgi.daemonize.log"
touchfile="${DIR}/touchforlogrotate"


DATE=`date -d "yesterday" +"%Y%m%d"`
destlogpath="${LOGDIR}/uwsgi.daemonize.${DATE}.log"

mv $sourcelogpath $destlogpath
touch $touchfile