#!/bin/bash

i="0"
while [ "$i" -lt 60 ]
do
  if [ ps up `cat /tmp/gestionPoulaillerRunning.pid ` >/dev/null ]
    then
      echo "Python process already running" >> /var/log/application.log
  else
      /usr/bin/python /home/pi/Developpement/Poulailler/gestionPoulaillier.py
  fi
  i=$[$i+1]
  sleep 1
done
