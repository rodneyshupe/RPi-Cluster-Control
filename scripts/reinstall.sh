#!/bin/bash

BASE_PATH="$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"

sudo systemctl is-active --quiet status_service.service && sudo systemctl stop status_service.service
sudo systemctl is-active --quiet state_service.service && sudo systemctl stop state_service.service
sudo systemctl is-active --quiet status_led_display.service && sudo systemctl stop status_led_display.service

if [ -e /lib/systemd/system/master_control.service ]
then
  sudo systemctl is-active --quiet master_control.service && sudo systemctl stop master_control.service
  SETUP_PARAM="master"
fi

rm -Rf "$BASE_PATH"
git clone https://github.com/rodneyshupe/RPi-Cluster-Control.git "$BASE_PATH"
chown -R pi:pi "$BASE_PATH"
chmod +x "$BASE_PATH/scripts/"*.sh

"$BASE_PATH/scripts/setup.sh" $SETUP_PARAM
