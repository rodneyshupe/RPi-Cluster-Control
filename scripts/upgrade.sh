#!/bin/bash

BASE_PATH="$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"

sudo systemctl is-active --quiet status_service.service && sudo systemctl stop status_service.service
sudo systemctl is-active --quiet state_service.service && sudo systemctl stop state_service.service
sudo systemctl is-active --quiet status_led_display.service && sudo systemctl stop status_led_display.service
sudo systemctl is-active --quiet master_control.service && sudo systemctl stop master_control.service

cd "$BASE_PATH"
git reset --hard
git pull

chmod +x "$BASE_PATH/scripts/"*.sh

sudo systemctl start status_service.service
sudo systemctl start state_service.service
sudo systemctl start status_led_display.service
if [ -f /lib/systemd/system/master_control.service ]
then
  sudo systemctl start master_control.service
fi
