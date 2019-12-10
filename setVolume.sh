#!/usr/bin/env bash

ACTION=$1
VOLUME=`cat volume.txt`

if [ $ACTION = 'up' ];then
  VOLUME=$((VOLUME+1))
  if [ $VOLUME -gt 100 ];then
    VOLUME=101
  fi

elif [ $ACTION = 'down' ];then
  VOLUME=$((VOLUME-1))
  if [ $VOLUME -lt 0 ];then
    VOLUME=-1
  fi

elif [ $ACTION = 'zero' ];then
  VOLUME=0

fi

echo $VOLUME  > volume.txt

