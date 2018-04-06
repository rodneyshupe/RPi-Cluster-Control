#!/bin/bash

#DEPLOY_PATH="/home/pi/StatusLED"
DEPLOY_PATH="~/StatusLED"
TEMP_DIR="/tmp/deploy"

rm -R "$TEMP_DIR"
mkdir "$TEMP_DIR"

find . -type f | grep -Ev '(\.git|\.DS_Store|deploy.sh|tests\/)' |
    grep -v -f <(sed 's/\([.|]\)/\\\1/g; s/\?/./g ; s/\*/.*/g' .gitignore) |
    while IFS= read -r filepath ; do
      file=$(basename "$filepath")
      cp $file "$TEMP_DIR/"
    done

ping -c1 -W1 192.168.8.100 1>/dev/null 2>/dev/null
if [ $? == 0 ]
then
  ip_address=$(ifconfig eth0 | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')
  if [ "$ip_address" != "192.168.8.100" ]
  then
    echo "Deploying to entire cluster"
    sshpass -p rpicluster scp $TEMP_DIR/* pi@192.168.8.100:$DEPLOY_PATH
  else
    echo "Deploying to the rest of the cluster"
  fi
  sshpass -p rpicluster scp $TEMP_DIR/* pi@192.168.8.101:$DEPLOY_PATH
  sshpass -p rpicluster scp $TEMP_DIR/* pi@192.168.8.102:$DEPLOY_PATH
  sshpass -p rpicluster scp $TEMP_DIR/* pi@192.168.8.103:$DEPLOY_PATH
else
  ping -c1 -W1 192.168.1.100 1>/dev/null 2>/dev/null
  if [ $? == 0 ]
  then
    echo "Deploying to Masternode.  Will need to replicate from there"
    sshpass -p rpicluster scp /tmp/deploy/* pi@192.168.1.100:~/StatusLED
    sshpass -p rpicluster scp deploy.sh pi@192.168.1.100:~/StatusLED
  else
    echo "IPs not available."
  fi
fi
