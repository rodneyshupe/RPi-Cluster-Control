import re
import json

try:
    from urllib.request import urlopen, URLError
except ImportError:
    from urllib2 import urlopen, URLError

#Get Configuration
try:
    #Test for custom config
    import config_master_custom as CONFIG
except:
    #If custom config fails load default
    import config_master_default as CONFIG

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'lib'))
from lib_common import str_join, isnumeric

def host_method(method, node = ""):
    cmd_response = {}
    if len(node) > 0:
        cmd_response[node] = host_call(str_join("http://", CONFIG.API_HOSTS[node], method))
    else:
        cmd_response = {}
        if CONFIG.USE_MULTITREADING:
            # Note to run this on OSX High Seira execute the following before
            # launching python:
            # export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
            from multiprocessing import Pool
            args = []
            for host in CONFIG.API_HOSTS:
                cmd_url = str_join("http://", CONFIG.API_HOSTS[host], method)
                args.append(cmd_url)
            pool = Pool(CONFIG.THREADS)
            pool_response = pool.map(host_call, args)
            i = 0
            for host in CONFIG.API_HOSTS:
                cmd_response[host] = pool_response[i]
                i+=1
            pool.close()
        else:
            for host in CONFIG.API_HOSTS:
                cmd_url = str_join("http://", CONFIG.API_HOSTS[host], method)
                cmd_response[host] = host_call(cmd_url)
    return(cmd_response)

def host_call(cmd_url):
    try:
        response = urlopen(cmd_url, timeout = 1)
        cmd_response = json.loads(response.read())
    except URLError as e:
        print('Got an error code from ', cmd_url, ':', e.args)
        cmd_response = { 'error':e.args }
    return(cmd_response)

class master_status():
    line_width = -1

    def __init__(self, line_width = -1):
        self.line_width = line_width
        self.linetypes = {
            1: "Usage",
            2: "Uptime",
            3: "IP",
            4: "OS",
        }

    def get_hosts(self):
        return(CONFIG.API_HOSTS)

    def get_status(self, node = "", debug = False):
        method = str_join(":", CONFIG.STATUS_API_PORT, "/api/v1.0/status")
        if debug:
            method += "/debug"
        return(host_method(method, node))

    # TODO: Write unittests
    def get_status_line(self, line_types = [1, 2, 3, 4], node = "", line_width = -1):
        status = self.get_status(node)

        lines = {}
        if not isinstance(line_types, list):
            line_types = [ int(line_types) ]
        for line_type in line_types:
            lines[line_type] = {}
            for node in status:
                lines[line_type][node] = self._status_line(line_type, status[node])
        return(lines)

    def _status_line(self, line_type, status):
        switcher = {
            1: self._usage,
            2: self._uptime,
            3: self._ip,
            4: self._os,
        }
        # Get the function from switcher dictionary
        func = switcher.get(line_type, lambda x: "Errror: Invalid line type")
        # Execute the function
        return(func(status))

    def _line(self, hostname, data_string):
        line_width = self.line_width if (self.line_width >= 0) else (len(data_string) + len(hostname) + 2)
        info_width = min((line_width - (len(hostname) + 1)), (len(data_string) + 1))
        line_str = str_join(hostname, ":", data_string.rjust(info_width, " "))
        if self.line_width >= 0:
            if (len(line_str) > self.line_width) and ((len(line_str) - (len(hostname) + 1)) <  self.line_width):
                line_str = line_str[-self.line_width:]
            else:
                line_str = line_str[:self.line_width]
        return(line_str)

    def _line_uptime(self, hostname, uptime_str):
        line_width = self.line_width if (self.line_width >= 0) else (len(uptime_str) + len(hostname) + 9)
        line_str = str_join(hostname, " uptime: ", uptime_str)
        if len(line_str) > line_width:
            line_str = str_join(hostname, " uptime:", uptime_str)
        if len(line_str) > line_width:
            line_str = str_join(hostname, " up: ", uptime_str)
        if len(line_str) > line_width:
            line_str = str_join(hostname, " up:", uptime_str)
        if len(line_str) > line_width:
            line_str = self._line(hostname, uptime_str)
        return(line_str)

    def _os(self, status):
        try:
            line_str = self._line(status['hostname'], str_join(status['uname']['system'], " ", status['uname']['release']))
        except:
            if "hostname" in status:
                line_str = str_join(status['hostname'], ": Data Error")
            else:
                line_str = "Data Error"
        return(line_str)

    def _ip(self, status):
        try:
            line_str = self._line(status['hostname'], status['ip'])
        except:
            if "hostname" in status:
                line_str = str_join(status['hostname'], ": Data Error")
            else:
                line_str = "Data Error"
        return(line_str)

    def _usage(self, status):
        try:
            line_str = self._line(status['hostname'],
                str_join(int(round(status['cpu']['usage'])), "% ",
                int(round(status['ram']['percent_used'])), "% ",
                status['cpu']['temperature'], "C" if isnumeric(status['cpu']['temperature']) else ""))
        except:
            if "hostname" in status:
                line_str = str_join(status['hostname'], ": Data Error")
            else:
                line_str = "Data Error"
        return(line_str)

    def _uptime(self, status):
        try:
            line_str = self._line_uptime(status['hostname'], status['uptime'])
        except:
            if "hostname" in status:
                line_str = str_join(status['hostname'], ": Data Error")
            else:
                line_str = "Data Error"
        return(line_str)

    def shutdown(self, node = ""):
        return(host_method(str_join(":", CONFIG.STATUS_API_PORT, "/api/v1.0/shutdown"), node))

    def reboot(self, node = ""):
        return(host_method(str_join(":", CONFIG.STATUS_API_PORT, "/api/v1.0/shutdown/reboot"), node))


class master_led():
    def __init__(self):
        self.led_mode = "manual"
        self.led_state = "000"
        self.led_pattern = "solid"
        self.led_pattern_speed = 1

    def get_settings(self):
        settings = {
            "led_mode":self.led_mode,
            "led_state":self.led_state,
            "led_pattern":self.led_pattern,
            "led_pattern_speed":self.led_pattern_speed,
        }
        return(settings)

    def get_state(self, node = ""):
        settings = self.get_settings()
        settings["nodes"] = host_method(str_join(":", CONFIG.LED_API_PORT, "/api/v1.0/state"), node)
        return(settings)

    def set_state(self, state, node = ""):
        self.led_state = state
        settings = self.get_settings()
        settings["nodes"] = host_method(str_join(":", CONFIG.LED_API_PORT, "/api/v1.0/state/", state), node)
        return(settings)

    def set_mode(self, mode):
        self.led_mode = mode
        return(self.get_settings())

    def set_pattern(self, pattern, speed = -1):
        self.led_pattern = pattern
        self.led_mode = "pattern"
        if speed >= 0:
            if speed == 0:
                self.led_mode = "manual"
                self.led_pattern = "solid"
                self.led_pattern_speed = 1
            else:
                self.led_pattern_speed = speed
        return(self.get_settings())
