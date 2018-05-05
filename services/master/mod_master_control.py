#!/usr/bin/env python
""" Methods used to handle the functionality of the Master Service API """

import json
import os
import sys

try:
    from urllib.request import Request, urlopen, URLError
except ImportError:
    from urllib2 import Request, urlopen, URLError

#Get Configuration
try:
    #Test for custom config
    import config_master_custom as CONFIG
except ImportError:
    #If custom config fails load default
    import config_master_default as CONFIG

# pylint: disable=wrong-import-position
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'lib'))
from lib_common import str_join, isnumeric
# pylint: enable=wrong-import-position

def host_method(method, node=None, protocol="GET"):
    '''
    Wrappper to call requested method of a node or all nodes
    '''
    cmd_response = {}
    if node:
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
                args.append((cmd_url, protocol))
            pool = Pool(CONFIG.THREADS)
            pool_response = pool.map(host_call_wrapper, args)
            i = 0
            for host in CONFIG.API_HOSTS:
                cmd_response[host] = pool_response[i]
                i += 1
            pool.close()
        else:
            for host in CONFIG.API_HOSTS:
                cmd_url = str_join("http://", CONFIG.API_HOSTS[host], method)
                cmd_response[host] = host_call(cmd_url, protocol)
    return cmd_response

def host_call(cmd_url, protocol="GET"):
    '''
    Make HTTP call to host.
    '''
    try:
        request = Request(cmd_url, method=protocol)
        #request.get_method = lambda: protocol
        response = urlopen(request)
        #response = urlopen(cmd_url)
        cmd_response = json.loads(response.read())
    except URLError as url_error:
        print('Got an error code from ', cmd_url, ':', url_error.args)
        cmd_response = {'error': url_error.args}
    return cmd_response

def host_call_wrapper(args):
    '''
    This function is for the multiprocessing to handle the multiple parameters to host_call.
    '''
    return host_call(*args)

class MasterStatus():
    '''
    Class containg methods for status.
    '''
    line_width = -1

    def __init__(self, line_width=-1):
        self.line_width = line_width
        self.linetypes = {
            1: "Usage",
            2: "Uptime",
            3: "IP",
            4: "OS",
        }

    @classmethod
    def get_hosts(cls):
        '''
        Returns Hosts in Config file.
        '''
        return CONFIG.API_HOSTS

    @classmethod
    def get_status(cls, node=None, debug=False):
        '''
        Get the status for requested node(s)
        '''
        method = str_join(":", CONFIG.STATUS_API_PORT, "/api/v1.0/status")
        if debug:
            method += "/debug"
        return host_method(method, node, 'GET')

    # TODO: Write unittests
    def get_status_line(self, line_types=None, node=None, line_width=-1):
        '''
        Returns requested line types.
        '''
        if line_types is None:
            line_types = [1, 2, 3, 4]

        status = self.get_status(node)
        lines = {}
        if not isinstance(line_types, list):
            line_types = [int(line_types)]
        for line_type in line_types:
            lines[line_type] = {}
            for host in status:
                line = self._status_line(line_type, status[host])
                if line_width > 0:
                    line = line[:line_width]
                lines[line_type][host] = line
        return lines

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
        return func(status)

    def _line(self, hostname, data_string):
        if self.line_width >= 0:
            line_width = self.line_width
        else:
            line_width = len(data_string) + len(hostname) + 2

        info_width = min((line_width - (len(hostname) + 1)), (len(data_string) + 1))
        line_str = str_join(hostname, ":", data_string.rjust(info_width, " "))

        if self.line_width >= 0:
            if ((len(line_str) > self.line_width) and
                    ((len(line_str) - (len(hostname) + 1)) < self.line_width)):
                line_str = line_str[-self.line_width:]
            else:
                line_str = line_str[:self.line_width]

        return line_str

    def _line_uptime(self, hostname, uptime_str):
        if self.line_width >= 0:
            line_width = self.line_width
        else:
            line_width = len(uptime_str) + len(hostname) + 9
        line_str = str_join(hostname, " uptime: ", uptime_str)
        if len(line_str) > line_width:
            line_str = str_join(hostname, " uptime:", uptime_str)
        if len(line_str) > line_width:
            line_str = str_join(hostname, " up: ", uptime_str)
        if len(line_str) > line_width:
            line_str = str_join(hostname, " up:", uptime_str)
        if len(line_str) > line_width:
            line_str = self._line(hostname, uptime_str)
        return line_str

    def _os(self, status):
        try:
            line_str = self._line(status['hostname'],
                                  str_join(status['uname']['system'],
                                           " ",
                                           status['uname']['release']))
        except KeyError:
            if "hostname" in status:
                line_str = str_join(status['hostname'], ": Data Error")
            else:
                line_str = "Data Error"
        return line_str

    def _ip(self, status):
        try:
            line_str = self._line(status['hostname'], status['ip'])
        except KeyError:
            if "hostname" in status:
                line_str = str_join(status['hostname'], ": Data Error")
            else:
                line_str = "Data Error"
        return line_str

    def _usage(self, status):
        try:
            line_str = self._line(status['hostname'],
                                  str_join(int(round(status['cpu']['usage'])), "% ",
                                           int(round(status['ram']['percent_used'])), "% ",
                                           status['cpu']['temperature'],
                                           "C" if isnumeric(status['cpu']['temperature']) else ""))
        except KeyError:
            if "hostname" in status:
                line_str = str_join(status['hostname'], ": Data Error")
            else:
                line_str = "Data Error"
        return line_str

    def _uptime(self, status):
        try:
            line_str = self._line_uptime(status['hostname'], status['uptime'])
        except KeyError:
            if "hostname" in status:
                line_str = str_join(status['hostname'], ": Data Error")
            else:
                line_str = "Data Error"
        return line_str

    @classmethod
    def shutdown(cls, node=None):
        '''
        Call Shutdown Method
        '''
        return host_method(str_join(":", CONFIG.STATUS_API_PORT, "/api/v1.0/shutdown"),
                           node,
                           'DELETE')

    @classmethod
    def reboot(cls, node=None):
        '''
        Call Reboot Method
        '''
        return host_method(str_join(":", CONFIG.STATUS_API_PORT, "/api/v1.0/shutdown/reboot"),
                           node,
                           'DELETE')


class MasterLed():
    '''
    Class containg methods for LED control.
    '''
    def __init__(self):
        self.led_mode = "manual"
        self.led_state = "000"
        self.led_pattern = "solid"
        self.led_pattern_speed = 1

    def get_settings(self):
        '''
        Return all settings
        '''
        settings = {
            "led_mode":self.led_mode,
            "led_state":self.led_state,
            "led_pattern":self.led_pattern,
            "led_pattern_speed":self.led_pattern_speed,
        }
        return settings

    def get_state(self, node=None):
        '''
        Get the current state from requested node(s)
        '''
        settings = self.get_settings()
        settings["nodes"] = host_method(str_join(":", CONFIG.LED_API_PORT, "/api/v1.0/state"),
                                        node,
                                        'GET')
        return settings

    def set_state(self, state, node=None):
        '''
        Set the state for the requested node(s)
        '''
        self.led_state = state
        settings = self.get_settings()
        settings["nodes"] = host_method(str_join(":",
                                                 CONFIG.LED_API_PORT,
                                                 "/api/v1.0/state/",
                                                 state),
                                        node, 'PATCH')
        return settings

    def set_mode(self, mode):
        '''
        Set the state for the mode
        '''
        self.led_mode = mode
        return self.get_settings()

    def set_pattern(self, pattern, speed=-1):
        '''
        Set the state for the pattern and optional speed
        '''
        self.led_pattern = pattern
        self.led_mode = "pattern"
        if speed >= 0:
            if speed == 0:
                self.led_mode = "manual"
                self.led_pattern = "solid"
                self.led_pattern_speed = 1
            else:
                self.led_pattern_speed = speed
        return self.get_settings()
