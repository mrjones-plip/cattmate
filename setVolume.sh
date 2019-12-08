#!/usr/bin/env bash

ACTION=$1
VOLUME=`cat volume.txt`

if [ $ACTION = 'up' ];then
  VOLUME=$((VOLUME+1))
  echo $VOLUME  > volume.txt
elif [ $ACTION = 'down' ];then
  VOLUME=$((VOLUME-1))
  echo $VOLUME  > volume.txt
elif [ $ACTION = 'zero' ];then
  echo 0 > volume.txt
fi

