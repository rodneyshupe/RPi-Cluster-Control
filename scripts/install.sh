#!/bin/bash

function install_systemd {
  SERVICE=$1

  BASE_PATH="$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"

  sudo cp "$BASE_PATH/scripts/systemd/$SERVICE" /lib/systemd/system/
  sudo chmod 644 /lib/systemd/system/$SERVICE

  sudo sed -i -e "s#RPICLUSTER_ROOTDIR#$BASE_PATH#g" /lib/systemd/system/$SERVICE

  sudo systemctl daemon-reload
  sudo systemctl enable $SERVICE
  sudo systemctl start $SERVICE
  sudo systemctl status $SERVICE
}

DIR="$(dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"

sudo pip install flask flask_restful
sudo pip install psutil

chmod +x "$DIR/services/status/service_status_api.py"
chmod +x "$DIR/services/status_led/service_state_api.py"
chmod +x "$DIR/services/status_led/service_display.py"

install_systemd status_service.service
install_systemd state_service.service
install_systemd status_led_display.service

if [[ "$@" == "master" ]]
then
  chmod +x "$DIR/services/master/service_master_api.py"
  install_systemd master_control.service
fi

sudo netstat -pant | grep 500
