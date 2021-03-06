#!/usr/bin/env python
"""
Custom Config File for Master Control API
"""

MASTER_API_PORT = 5001
STATUS_API_PORT = 5002
LED_API_PORT = 5003

USE_MULTITREADING = True
THREADS = 4

APP_DEBUG = True

API_HOSTS = {
    'rpi0':'192.168.8.100',
    'rpi1':'192.168.8.101',
    'rpi2':'192.168.8.102',
    'rpi3':'192.168.8.103',
}
