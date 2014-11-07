#!/bin/bash

PORT=8888
DIR=`pwd`
DATADIR=`pwd`/data
LOGFILE=`pwd`/logfile.txt
PIDFILE=`pwd`/mini_http.pid

echo "DATA DIR: "${DATADIR}
echo "LOG FILE: "${LOGFILE}
echo "PID FILE: "${PIDFILE}

mkdir -p $DATADIR

bin/mini-httpd -d $DIR -dd $DATADIR -l $LOGFILE -i $PIDFILE -c '*.cgi' -p $PORT

echo "http://$HOSTNAME:$PORT"
