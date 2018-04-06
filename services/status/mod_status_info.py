#!/usr/bin/env python

import sys
import psutil
import platform
import socket
import subprocess
import re

#from subprocess import PIPE, Popen

class status_info():

    def get_uptime(self):
        #uptime | sed 's/^.*up *//;s/, *[0-9]* user.*$/m/;s/ day[^0-9]*/d, /;s/ \([hms]\).*m$/\1/;s/:/h, /'
        uptime_str = subprocess.check_output('uptime').decode("utf-8")
        uptime_str = re.sub("^.*up *", "", uptime_str)
        uptime_str = re.sub(", *[0-9]* user.*$","m", uptime_str)
        uptime_str = re.sub(" minm", "m", uptime_str)
        uptime_str = re.sub(" day[^0-9]*", "d ", uptime_str)
        uptime_str = re.sub(" \([hms]\).*m$", "\1", uptime_str)
        uptime_str = re.sub(":", "h ", uptime_str).strip()
        return(uptime_str)

    # Return CPU temperature as a character string
    def get_cpu_temperature(self):
        try:
            output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode("utf-8")
            return round(float(output[output.index('=') + 1:output.rindex("'")]), 1)
        except:
            return "n/a"

    def get_ram_info(self):
        try:
            free = subprocess.check_output('free').decode('utf-8')
            lines = free.split('\n')
            ram_stats = lines[1].split()[1:4]
            ram_info = {'method':'free', 'total':int(ram_stats[0]), 'used':int(ram_stats[1]), 'free':int(ram_stats[2]), 'percent_used': round((float(int(ram_stats[1]))/int(ram_stats[0])) * 100, 1)}
        except:
            try:
                ram_stats = psutil.virtual_memory()
                ram_info = {'method':'psutil', 'total':int(ram_stats[0]), 'used':int(ram_stats[3]), 'free':int(ram_stats[1]), 'percent_used':ram_stats[2]}
            except:
                ram_info = {'method':'n/a', 'total':None, 'used':None, 'free':None, 'percent_used':None}
        return(ram_info)

    def get_ram_percent(self):
        ram_info = self.get_ram_info()
        ram_percent_used = ram_info['percent_used']
        return(ram_percent_used)

    # Return % of CPU used by user as a character string
    def get_cpu_usage(self):
        return(psutil.cpu_percent())

    def get_hostname(self):
        return(socket.getfqdn()[:4]) # socket.gethostname()

    def get_ip_address(self):
        #This is a bit hackish but returns the correct address as socket.gethostbyname(hostname) return 127.0.1.1
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return(ip_address)

    def get_debug_info(self):
        debug_info = {
            'python_vesion':"%s.%s.%s" % sys.version_info[:3],
            'psutil_version':psutil.__version__,
        }
        return(debug_info)

    def get_uname(self):
        uname = platform.uname()
        uname_info = {
            'system':uname[0],
            'node':uname[1],
            'release':uname[2],
            'version':uname[3],
            'machine':uname[4],
            'processor':uname[5],
        }
        return(uname_info)

    def get_info(self, debug=False):
        info = {
            'hostname':self.get_hostname(),
            'ip':self.get_ip_address(),
            'uptime':self.get_uptime(),
            'cpu':{
                'temperature':self.get_cpu_temperature(),
                'usage':psutil.cpu_percent(),
            },
            'cpu_count': psutil.cpu_count(),
            'uname':self.get_uname(),
            'ram':self.get_ram_info(),
        }
        if debug:
            info['debug'] = self.get_debug_info()
        return(info)
