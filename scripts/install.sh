#!/bin/bash

if [ "$HOSTNAME" = rpi0 ]
then
  SETUP_PARAM="master"
fi

BASE_PATH="~/cluster_control"

rm -Rf "$BASE_PATH"
git clone https://github.com/rodneyshupe/RPi-Cluster-Control.git "$BASE_PATH"
chown -R pi:pi "$BASE_PATH"
chmod +x "$BASE_PATH/scripts/"*.sh

"$BASE_PATH/scripts/setup.sh" $SETUP_PARAM
