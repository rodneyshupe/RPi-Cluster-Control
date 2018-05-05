#!/usr/bin/env python
# pylint: disable=line-too-long
"""
Test data for Status API calls used for mocking in unit tests
"""
TESTDATA = {
    'http://192.168.8.100:5002/api/v1.0/status':'{"cpu":{"temperature": 52.8,"usage": 3.7},"hostname": "rpi0","ip": "192.168.8.100","ram":{"free": 709013504,"percent_used": 30.0,"total": 1024319488,"used": 190210048},"uname":{"machine": "armv7l","node": "rpi0","processor": "","release": "4.9.80-v7+","system": "Linux","version": "#1098 SMP Fri Mar 9 19:11:42 GMT 2018"},"uptime": "15m"}',
    'http://192.168.8.100:5002/api/v1.0/status/debug':'{"cpu":{"temperature": 52.8,"usage": 3.7},"debug":{"psutil_version": "5.4.3","python_vesion": "2.7.13"},"hostname": "rpi0","ip": "192.168.8.100","ram":{"free": 709013504,"percent_used": 30.1,"total": 1024319488,"used": 190210048},"uname":{"machine": "armv7l","node": "rpi0","processor": "","release": "4.9.80-v7+","system": "Linux","version": "#1098 SMP Fri Mar 9 19:11:42 GMT 2018"},"uptime": "15m"}',
    'http://192.168.8.100:5002/api/v1.0/debug':'{"psutil_version": "5.4.3","python_vesion": "2.7.13"}',
    'http://192.168.8.100:5002/api/v1.0/shutdown':'{"action":"Shutdown", "command":"/usr/bin/sudo /sbin/shutdown now", "result":"ok"}',
    'http://192.168.8.100:5002/api/v1.0/shutdown/reboot':'{"action":"Reboot", "command":"/usr/bin/sudo /sbin/shutdown -r now", "result":"ok"}',
    'http://192.168.8.101:5002/api/v1.0/status':'{"cpu":{"temperature": 53.8,"usage": 2.6},"hostname": "rpi1","ip": "192.168.8.101","ram":{"free": 709013504,"percent_used": 30.1,"total": 1024319488,"used": 190210048},"uname":{"machine": "armv7l","node": "rpi1","processor": "","release": "4.9.80-v7+","system": "Linux","version": "#1098 SMP Fri Mar 9 19:11:42 GMT 2018"},"uptime": "10d 12h 20m"}',
    'http://192.168.8.101:5002/api/v1.0/status/debug':'{"cpu":{"temperature": 53.8,"usage": 2.6},"debug":{"psutil_version": "5.4.3","python_vesion": "2.7.13"},"hostname": "rpi3","ip": "192.168.8.101","ram":{"free": 709013504,"percent_used": 30.1,"total": 1024319488,"used": 190210048},"uname":{"machine": "armv7l","node": "rpi1","processor": "","release": "4.9.80-v7+","system": "Linux","version": "#1098 SMP Fri Mar 9 19:11:42 GMT 2018"},"uptime": "10d 12h 20m"}',
    'http://192.168.8.101:5002/api/v1.0/debug':'{"psutil_version": "5.4.3","python_vesion": "2.7.13"}',
    'http://192.168.8.101:5002/api/v1.0/shutdown':'{"action":"Shutdown", "command":"/usr/bin/sudo /sbin/shutdown now", "result":"ok"}',
    'http://192.168.8.101:5002/api/v1.0/shutdown/reboot':'{"action":"Reboot", "command":"/usr/bin/sudo /sbin/shutdown -r now", "result":"ok"}',
    'http://192.168.8.102:5002/api/v1.0/status':'{"cpu":{"temperature": 54.8,"usage": 2.7},"hostname": "rpi2","ip": "192.168.8.102","ram":{"free": 709013504,"percent_used": 30.2,"total": 1024319488,"used": 190210048},"uname":{"machine": "armv7l","node": "rpi2","processor": "","release": "4.9.80-v7+","system": "Linux","version": "#1098 SMP Fri Mar 9 19:11:42 GMT 2018"},"uptime": "2d 17h 01m"}',
    'http://192.168.8.102:5002/api/v1.0/status/debug':'{"cpu":{"temperature": 54.8,"usage": 2.7},"debug":{"psutil_version": "5.4.3","python_vesion": "2.7.13"},"hostname": "rpi3","ip": "192.168.8.102","ram":{"free": 709013504,"percent_used": 30.2,"total": 1024319488,"used": 190210048},"uname":{"machine": "armv7l","node": "rpi2","processor": "","release": "4.9.80-v7+","system": "Linux","version": "#1098 SMP Fri Mar 9 19:11:42 GMT 2018"},"uptime": "2d 17h 01m"}',
    'http://192.168.8.102:5002/api/v1.0/debug':'{"psutil_version": "5.4.3","python_vesion": "2.7.13"}',
    'http://192.168.8.102:5002/api/v1.0/shutdown':'{"action":"Shutdown", "command":"/usr/bin/sudo /sbin/shutdown now", "result":"ok"}',
    'http://192.168.8.102:5002/api/v1.0/shutdown/reboot':'{"action":"Reboot", "command":"/usr/bin/sudo /sbin/shutdown -r now", "result":"ok"}',
    'http://192.168.8.103:5002/api/v1.0/status':'{"cpu":{"temperature": 55.8,"usage": 2.7},"hostname": "rpi3","ip": "192.168.8.103","ram":{"free": 709013504,"percent_used": 30.3,"total": 1024319488,"used": 190210048},"uname":{"machine": "armv7l","node": "rpi3","processor": "","release": "4.9.80-v7+","system": "Linux","version": "#1098 SMP Fri Mar 9 19:11:42 GMT 2018"},"uptime": "3h 02m"}',
    'http://192.168.8.103:5002/api/v1.0/status/debug':'{"cpu":{"temperature": 55.8,"usage": 2.7},"debug":{"psutil_version": "5.4.3","python_vesion": "2.7.13"},"hostname": "rpi3","ip": "192.168.8.103","ram":{"free": 709013504,"percent_used": 30.3,"total": 1024319488,"used": 190210048},"uname":{"machine": "armv7l","node": "rpi3","processor": "","release": "4.9.80-v7+","system": "Linux","version": "#1098 SMP Fri Mar 9 19:11:42 GMT 2018"},"uptime": "3h 02m"}',
    'http://192.168.8.103:5002/api/v1.0/debug':'{"psutil_version": "5.4.3","python_vesion": "2.7.13"}',
    'http://192.168.8.103:5002/api/v1.0/shutdown':'{"action":"Shutdown", "command":"/usr/bin/sudo /sbin/shutdown now", "result":"ok"}',
    'http://192.168.8.103:5002/api/v1.0/shutdown/reboot':'{"action":"Reboot", "command":"/usr/bin/sudo /sbin/shutdown -r now", "result":"ok"}',
}
