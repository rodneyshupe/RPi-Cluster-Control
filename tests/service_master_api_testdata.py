#!/usr/bin/env python

testdata = {
    'http://192.168.8.100:5001/api/v1.0/nodes':'{}',
    'http://192.168.8.100:5001/api/v1.0/status':'{}',
    'http://192.168.8.100:5001/api/v1.0/status/debug':'{}',
    'http://192.168.8.100:5001/api/v1.0/status/rpi0':'{}',
    'http://192.168.8.100:5001/api/v1.0/status/rpi1':'{}',
    'http://192.168.8.100:5001/api/v1.0/status/rpi2':'{}',
    'http://192.168.8.100:5001/api/v1.0/status/rpi3':'{}',
    'http://192.168.8.100:5001/api/v1.0/status/debug/rpi0':'{}',
    'http://192.168.8.100:5001/api/v1.0/status/debug/rpi1':'{}',
    'http://192.168.8.100:5001/api/v1.0/status/debug/rpi2':'{}',
    'http://192.168.8.100:5001/api/v1.0/status/debug/rpi3':'{}',
    'http://192.168.8.100:5001/api/v1.0/shutdown':'{}',
    'http://192.168.8.100:5001/api/v1.0/shutdown/reboot':'{}',
    'http://192.168.8.100:5001/api/v1.0/shutdown/reboot/rpi0':'{}',
    'http://192.168.8.100:5001/api/v1.0/shutdown/reboot/rpi1':'{}',
    'http://192.168.8.100:5001/api/v1.0/shutdown/reboot/rpi2':'{}',
    'http://192.168.8.100:5001/api/v1.0/shutdown/reboot/rpi3':'{}',
    'http://192.168.8.100:5001/api/v1.0/get_led':'{}',
    'http://192.168.8.100:5001/api/v1.0/get_led/rpi0':'{}',
    'http://192.168.8.100:5001/api/v1.0/get_led/rpi1':'{}',
    'http://192.168.8.100:5001/api/v1.0/get_led/rpi2':'{}',
    'http://192.168.8.100:5001/api/v1.0/get_led/rpi3':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/000':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/020':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/mode/auto':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/mode/manual':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/mode/solid':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/pattern/solid':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/pattern/blink':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/pattern/rotate':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/pattern/rotate/2':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/pattern/rotate/2.5':'{}',
    'http://192.168.8.100:5001/api/v1.0/set_led/pattern/blink/1.5':'{}',
}

test_results = {
    'get_status': {
        'rpi0': {
            'cpu': {'temperature': 52.8, 'usage': 3.7},
            'hostname': 'rpi0',
            'ip': '192.168.8.100',
            'ram': {'free': 709013504, 'percent_used': 30.0, 'total': 1024319488, 'used': 190210048},
            'uname': {
                'machine': 'armv7l',
                'node': 'rpi0',
                'processor': '',
                'release': '4.9.80-v7+',
                'system': 'Linux',
                'version': '#1098 SMP Fri Mar 9 19:11:42 GMT 2018'
            },
            'uptime': '15m'
        },
        'rpi1': {
            'cpu': {'temperature': 53.8, 'usage': 2.6},
            'hostname': 'rpi1',
            'ip': '192.168.8.101',
            'ram': {'free': 709013504, 'percent_used': 30.1, 'total': 1024319488, 'used': 190210048},
            'uname': {
                'machine': 'armv7l',
                'node': 'rpi1',
                'processor': '',
                'release': '4.9.80-v7+',
                'system': 'Linux',
                'version': '#1098 SMP Fri Mar 9 19:11:42 GMT 2018'
            },
            'uptime': '10d 12h 20m'
        },
        'rpi2': {
            'cpu': {'temperature': 54.8, 'usage': 2.7},
            'hostname': 'rpi2',
            'ip': '192.168.8.102',
            'ram': {'free': 709013504, 'percent_used': 30.2, 'total': 1024319488, 'used': 190210048},
            'uname': {
                'machine': 'armv7l',
                'node': 'rpi2',
                'processor': '',
                'release': '4.9.80-v7+',
                'system': 'Linux',
                'version': '#1098 SMP Fri Mar 9 19:11:42 GMT 2018'
            },
            'uptime': '2d 17h 01m'
        },
        'rpi3': {
            'cpu': {'temperature': 55.8, 'usage': 2.7},
            'hostname': 'rpi3',
            'ip': '192.168.8.103',
            'ram': {'free': 709013504, 'percent_used': 30.3, 'total': 1024319488, 'used': 190210048},
            'uname': {
                'machine': 'armv7l',
                'node': 'rpi3',
                'processor': '',
                'release': '4.9.80-v7+',
                'system': 'Linux',
                'version': '#1098 SMP Fri Mar 9 19:11:42 GMT 2018'
            },
            'uptime': '3h 02m'
        }
    },
    'shutdown': {
        'rpi0': {'action': 'Shutdown', 'command': '/usr/bin/sudo /sbin/shutdown now', 'result': 'ok'},
        'rpi1': {'action': 'Shutdown', 'command': '/usr/bin/sudo /sbin/shutdown now', 'result': 'ok'},
        'rpi2': {'action': 'Shutdown', 'command': '/usr/bin/sudo /sbin/shutdown now', 'result': 'ok'},
        'rpi3': {'action': 'Shutdown', 'command': '/usr/bin/sudo /sbin/shutdown now', 'result': 'ok'}
    },
    'reboot': {
        'rpi0': {'action': 'Reboot', 'command': '/usr/bin/sudo /sbin/shutdown -r now', 'result': 'ok'},
        'rpi1': {'action': 'Reboot', 'command': '/usr/bin/sudo /sbin/shutdown -r now', 'result': 'ok'},
        'rpi2': {'action': 'Reboot', 'command': '/usr/bin/sudo /sbin/shutdown -r now', 'result': 'ok'},
        'rpi3': {'action': 'Reboot', 'command': '/usr/bin/sudo /sbin/shutdown -r now', 'result': 'ok'}
    },
    'get_state': {
        'led_mode': 'manual',
        'led_state': '000',
        'led_pattern': 'solid',
        'led_pattern_speed': 1,
        'nodes': {
            'rpi0': {'state': '000'},
            'rpi1': {'state': '001'},
            'rpi2': {'state': '002'},
            'rpi3': {'state': '010'}
        }
    },
    'status_lines': {
        -1: {
            'line_os': {
                'rpi0': 'rpi0: Linux 4.9.80-v7+',
                'rpi1': 'rpi1: Linux 4.9.80-v7+',
                'rpi2': 'rpi2: Linux 4.9.80-v7+',
                'rpi3': 'rpi3: Linux 4.9.80-v7+',
            },
            'line_ip': {
                'rpi0': 'rpi0: 192.168.8.100',
                'rpi1': 'rpi1: 192.168.8.101',
                'rpi2': 'rpi2: 192.168.8.102',
                'rpi3': 'rpi3: 192.168.8.103',
            },
            'line_usage': {
                'rpi0': 'rpi0: 4% 30% 52.8C',
                'rpi1': 'rpi1: 3% 30% 53.8C',
                'rpi2': 'rpi2: 3% 30% 54.8C',
                'rpi3': 'rpi3: 3% 30% 55.8C',
            },
            'line_uptime': {
                'rpi0': 'rpi0 uptime: 15m',
                'rpi1': 'rpi1 uptime: 10d 12h 20m',
                'rpi2': 'rpi2 uptime: 2d 17h 01m',
                'rpi3': 'rpi3 uptime: 3h 02m',
            },
        },
        40: {
            'line_os': {
                'rpi0': 'rpi0: Linux 4.9.80-v7+',
                'rpi1': 'rpi1: Linux 4.9.80-v7+',
                'rpi2': 'rpi2: Linux 4.9.80-v7+',
                'rpi3': 'rpi3: Linux 4.9.80-v7+',
            },
            'line_ip': {
                'rpi0': 'rpi0: 192.168.8.100',
                'rpi1': 'rpi1: 192.168.8.101',
                'rpi2': 'rpi2: 192.168.8.102',
                'rpi3': 'rpi3: 192.168.8.103',
            },
            'line_usage': {
                'rpi0': 'rpi0: 4% 30% 52.8C',
                'rpi1': 'rpi1: 3% 30% 53.8C',
                'rpi2': 'rpi2: 3% 30% 54.8C',
                'rpi3': 'rpi3: 3% 30% 55.8C',
            },
            'line_uptime': {
                'rpi0': 'rpi0 uptime: 15m',
                'rpi1': 'rpi1 uptime: 10d 12h 20m',
                'rpi2': 'rpi2 uptime: 2d 17h 01m',
                'rpi3': 'rpi3 uptime: 3h 02m',
            },
        },
        20: {
            'line_os': {
                'rpi0': 'pi0:Linux 4.9.80-v7+',
                'rpi1': 'pi1:Linux 4.9.80-v7+',
                'rpi2': 'pi2:Linux 4.9.80-v7+',
                'rpi3': 'pi3:Linux 4.9.80-v7+',
            },
            'line_ip': {
                'rpi0': 'rpi0: 192.168.8.100',
                'rpi1': 'rpi1: 192.168.8.101',
                'rpi2': 'rpi2: 192.168.8.102',
                'rpi3': 'rpi3: 192.168.8.103',
            },
            'line_usage': {
                'rpi0': 'rpi0: 4% 30% 52.8C',
                'rpi1': 'rpi1: 3% 30% 53.8C',
                'rpi2': 'rpi2: 3% 30% 54.8C',
                'rpi3': 'rpi3: 3% 30% 55.8C',
            },
            'line_uptime': {
                'rpi0': 'rpi0 uptime: 15m',
                'rpi1': 'rpi1 up: 10d 12h 20m',
                'rpi2': 'rpi2 up: 2d 17h 01m',
                'rpi3': 'rpi3 uptime: 3h 02m',
            },
        },
        16: {
            'line_os': {
                'rpi0': 'rpi0:Linux 4.9.8',
                'rpi1': 'rpi1:Linux 4.9.8',
                'rpi2': 'rpi2:Linux 4.9.8',
                'rpi3': 'rpi3:Linux 4.9.8',
            },
            'line_ip': {
                'rpi0': 'i0:192.168.8.100',
                'rpi1': 'i1:192.168.8.101',
                'rpi2': 'i2:192.168.8.102',
                'rpi3': 'i3:192.168.8.103',
            },
            'line_usage': {
                'rpi0': 'pi0:4% 30% 52.8C',
                'rpi1': 'pi1:3% 30% 53.8C',
                'rpi2': 'pi2:3% 30% 54.8C',
                'rpi3': 'pi3:3% 30% 55.8C',
            },
            'line_uptime': {
                'rpi0': 'rpi0 uptime: 15m',
                'rpi1': 'rpi1:10d 12h 20m',
                'rpi2': 'rpi2: 2d 17h 01m',
                'rpi3': 'rpi3 up: 3h 02m',
            },
        },
    },
}

def contains(string, ignore_keywords):
    check = False
    for keyword in ignore_keywords:
        if string.find(keyword) >= 0:
            print("found ", keyword, " in ", string)
            check = True
    return(check)

def populate_testdata(ignore_keywords = ['shutdown', 'reboot']):
    for url in testdata:
        print(url)
        if not contains(url, ignore_keywords):
            print(url)
            from urllib.request import urlopen
            response = urlopen(url, timeout = 1)
            testdata[url] = response.read()
    return(True)

def print_testdata(refresh = False, ignore_keywords = ['shutdown', 'reboot']):
    if refresh:
        print("Refreshing...")
        populate_testdata(ignore_keywords)
    print(testdata)

import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "refresh":
        print_testdata(True)
    elif sys.argv[1] == "print":
        print_testdata()
