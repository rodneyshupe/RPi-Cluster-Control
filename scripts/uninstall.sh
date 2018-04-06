#!/bin/bash

function uninstall_systemd {
  SERVICE=$1
  systemctl stop $SERVICE
  systemctl disable $SERVICE
  rm /etc/systemd/system/$SERVICE
}

uninstall_systemd status_service.service
uninstall_systemd state_service.service
uninstall_systemd display.service

systemctl daemon-reload
systemctl reset-failed
