#!/usr/bin/env python
""" Module containing functionality for the status API """

import sys
import platform
import socket
import subprocess
import re
import psutil

class StatusInfo():
    """
    Status class containing methods for retrieving and returning status info
    """

    @classmethod
    def get_uptime(cls):
        """
        Get the machines uptime.
        This method requires the command uptime
        """

        uptime_str = subprocess.check_output('uptime').decode("utf-8")
        # This simulates the command:
        # sed 's/^.*up *//;s/, *[0-9]* user.*$/m/;s/ day[^0-9]*/d, /;s/ \([hms]\).*m$/\1/;s/:/h, /'
        uptime_str = re.sub("^.*up *", "", uptime_str)
        uptime_str = re.sub(", *[0-9]* user.*$", "m", uptime_str)
        uptime_str = re.sub(" minm", "m", uptime_str)
        uptime_str = re.sub(" day[^0-9]*", "d ", uptime_str)
        uptime_str = re.sub(r" \([hms]\).*m$", "\1", uptime_str)
        uptime_str = re.sub(":", "h ", uptime_str).strip()
        return uptime_str

    # Return CPU temperature as a character string
    @classmethod
    def get_cpu_temperature(cls):
        """
        Get the machines cpu tempurature.
        This method requires the command vcgencmd
        """
        try:
            output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode("utf-8")
            return round(float(output[output.index('=') + 1:output.rindex("'")]), 1)
        except FileNotFoundError:
            return "n/a"

    @classmethod
    def get_ram_info(cls):
        """
        Get the machines memory info.
        This method trys to use the command free and if that fails it leverages the psutil module.
        """
        try:
            free = subprocess.check_output('free').decode('utf-8')
            lines = free.split('\n')
            ram_stats = lines[1].split()[1:4]
            ram_info = {
                'method':'free',
                'total':int(ram_stats[0]),
                'used':int(ram_stats[1]),
                'free':int(ram_stats[2]),
                'percent_used': round((float(int(ram_stats[1]))/int(ram_stats[0])) * 100, 1)
            }
        except (FileNotFoundError, AttributeError):
            try:
                ram_stats = psutil.virtual_memory()
                ram_info = {
                    'method':'psutil',
                    'total':int(ram_stats[0]),
                    'used':int(ram_stats[3]),
                    'free':int(ram_stats[1]),
                    'percent_used':ram_stats[2]
                }
            except IndexError:
                ram_info = {
                    'method':'n/a',
                    'total':None,
                    'used':None,
                    'free':None,
                    'percent_used':None
                }
        return ram_info

    def get_ram_percent(self):
        """
        Return % of RAM used by machine as a character string
        """
        ram_info = self.get_ram_info()
        ram_percent_used = ram_info['percent_used']
        return ram_percent_used

    @classmethod
    def get_cpu_usage(cls):
        """
        Return % of CPU used by machine as a character string
        """
        return psutil.cpu_percent()

    @classmethod
    def get_hostname(cls):
        """
        Return machine hostname
        """
        return socket.getfqdn()[:4] # socket.gethostname()

    @classmethod
    def get_ip_address(cls):
        """
        Return ip address as a character string
        """
        """
        This is a bit hackish but returns the correct address as
        socket.gethostbyname(hostname) return 127.0.1.1
        """
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_socket.connect(("8.8.8.8", 80))
        ip_address = test_socket.getsockname()[0]
        test_socket.close()
        return ip_address

    @classmethod
    def get_debug_info(cls):
        """
        Return some useful info for debugging.
        """
        debug_info = {
            'python_vesion':"%s.%s.%s" % sys.version_info[:3],
            'psutil_version':psutil.__version__,
            # FUTURE_TODO: Add versioning info of API versions
        }
        return debug_info

    @classmethod
    def get_uname(cls):
        """
        Return uname (OS) info of the machine
        """
        uname = platform.uname()
        uname_info = {
            'system':uname[0],
            'node':uname[1],
            'release':uname[2],
            'version':uname[3],
            'machine':uname[4],
            'processor':uname[5],
        }
        return uname_info

    def get_info(self, debug=False):
        """
        Return all the status info of the machine as a Dictionary
        """
        info = {
            'hostname': self.get_hostname(),
            'ip': self.get_ip_address(),
            'uptime': self.get_uptime(),
            'cpu':{
                'temperature': self.get_cpu_temperature(),
                'usage':psutil.cpu_percent(),
            },
            'cpu_count': psutil.cpu_count(),
            'uname': self.get_uname(),
            'ram': self.get_ram_info(),
        }
        if debug:
            info['debug'] = self.get_debug_info()
        return info
