#!/usr/bin/env python
""" Default Configuration File for status API """

DEFAULT_LINE_WIDTH = 20
LCD_LINES_DEFAULT = 4

STATUS_API_PORT = 5002

APP_DEBUG = True

STATUS_API_HOSTS = {
    'rpi0':'192.168.8.100:5002',
    'rpi1':'192.168.8.101:5002',
    'rpi2':'192.168.8.102:5002',
    'rpi3':'192.168.8.103:5002',
}
