#!/usr/bin/env python

import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html
from unittest.mock import patch, Mock

import json
import urllib.request

import sys
#sys.path.append("..")
sys.path.append("../services/master")
import mod_master_control
import config_master_default as CONFIG

#Build testdata
import service_status_api_testdata
import service_state_api_testdata
TESTDATA = {}
for key in service_status_api_testdata.testdata:
    TESTDATA[key] = service_status_api_testdata.testdata[key]
for key in service_state_api_testdata.testdata:
    TESTDATA[key] = service_state_api_testdata.testdata[key]

import service_master_api_testdata

class UnitTests_mod_master_control(unittest.TestCase):

    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass

    # clean up logic for the test suite declared in the test module
    # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass

    # initialization logic
    # code that is executed before each test
    def setUp(self):
        self.master_led_default_settings = {
            "led_mode":"manual",
            "led_state":"000",
            "led_pattern":"solid",
            "led_pattern_speed":1,
        }
        self.maxDiff = None

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass

    # These function used used to mock the urlib.request.urlopen method
    def mock_call_urlopen(url, timeout):
        with patch('urllib.request.urlopen') as mocked_urlopen:
            mock_urlopen_return = Mock()
            try:
                return_value = TESTDATA[url]
            except:
                return_value = '{"error":"No test data for ' + url + '"}'
                raise ValueError('No test data for ' + url)

            mock_urlopen_return.read.return_value = return_value
            mocked_urlopen.return_value = mock_urlopen_return
            result = urllib.request.urlopen(url)
        return result

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_host_method(self, mock_urlopen):
        # Test mod_master_control.host_method(method, node = "")
        mod_master_control.CONFIG.USE_MULTITREADING = False
        result = mod_master_control.host_method(':5002/api/v1.0/status')
        self.assertEqual(result, service_master_api_testdata.test_results['get_status'])
        result = mod_master_control.host_method(':5002/api/v1.0/status', "rpi1")
        self.assertEqual(result, {'rpi1':service_master_api_testdata.test_results['get_status']['rpi1']})

        mod_master_control.CONFIG.USE_MULTITREADING = True
        result = mod_master_control.host_method(':5002/api/v1.0/status')
        self.assertEqual(result, service_master_api_testdata.test_results['get_status'])
        result = mod_master_control.host_method(':5002/api/v1.0/status', "rpi2")
        self.assertEqual(result, {'rpi2':service_master_api_testdata.test_results['get_status']['rpi2']})

        #ValueError
        with self.assertRaises(ValueError):
            mod_master_control.host_method('')
        with self.assertRaises(ValueError):
            mod_master_control.host_method('','')

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_host_call(self, mock_urlopen):
        with self.assertRaises(Exception):
            mod_master_control.host_method('')

    def test_mod_master_control_host_master_status_get_hosts(self):
        self.assertEqual(mod_master_control.master_status().get_hosts(),mod_master_control.CONFIG.API_HOSTS)

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_status_get_status(self, mock_urlopen):
        # Test get_status(node = "", debug = False)
        status = mod_master_control.master_status().get_status()
        self.assertEqual(status, service_master_api_testdata.test_results['get_status'])
        status = mod_master_control.master_status().get_status("rpi0")
        self.assertEqual(status, {'rpi0': service_master_api_testdata.test_results['get_status']['rpi0']})

        with self.assertRaises(TypeError):
            result = mod_master_control.master_status().get_status(1)
        with self.assertRaises(KeyError):
            state = mod_master_control.master_status().get_status("abc")

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_status_get_status_line(self, mock_urlopen):
        # Test get_status_line(line_types = [1, 2, 3, 4], node = "", line_width = -1)

        status = mod_master_control.master_status().get_status()
        line_types_list =[ [2,3], [1, 2, 3, 4], 2]
        line_type_keys = { 4:'line_os', 3:'line_ip', 1:'line_usage', 2:'line_uptime' }

        # Test all passed in
        for line_types in line_types_list:
            # Test multiple nodes at various lengths [-1, 40, 20, 16]
            for node in CONFIG.API_HOSTS:
                # Test node at various lengths [-1, 40, 20, 16]
                for line_width in service_master_api_testdata.test_results['status_lines']:
                    result = mod_master_control.master_status(line_width).get_status_line(line_types, node, line_width)
                    test_data = {}
                    if isinstance(line_types, list):
                        lines_types_for_loop = line_types
                    else:
                        lines_types_for_loop = [ line_types ]
                    for line_type in lines_types_for_loop:
                        test_data[line_type] = {node : service_master_api_testdata.test_results['status_lines'][line_width][line_type_keys[line_type]][node]}
                    self.assertEqual(result, test_data)

        # Test no node passed
        for line_types in line_types_list:
            # Test multiple nodes at various lengths [-1, 40, 20, 16]
            for line_width in service_master_api_testdata.test_results['status_lines']:
                result = mod_master_control.master_status(line_width).get_status_line(line_types = line_types, line_width = line_width)
                test_data = {}
                if isinstance(line_types, list):
                    lines_types_for_loop = line_types
                else:
                    lines_types_for_loop = [ line_types ]
                for line_type in lines_types_for_loop:
                    test_data[line_type] = {}
                    for node in CONFIG.API_HOSTS:
                        test_data[line_type][node] = service_master_api_testdata.test_results['status_lines'][line_width][line_type_keys[line_type]][node]
                self.assertEqual(result, test_data)

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_status__status_line(self, mock_urlopen):
        # Test _status_line(line_type, status)
        module = mod_master_control.master_status()
        line_types = { 4:'line_os', 3:'line_ip', 1:'line_usage', 2:'line_uptime' }

        status = mod_master_control.master_status().get_status()
        for line_type in range(1,4):
            # Test multiple nodes at various lengths [-1, 40, 20, 16]
            for node in CONFIG.API_HOSTS:
                # Test node at various lengths [-1, 40, 20, 16]
                for line_width in service_master_api_testdata.test_results['status_lines']:
                    result = mod_master_control.master_status(line_width)._status_line(line_type, status[node])
                    test_data = service_master_api_testdata.test_results['status_lines'][line_width][line_types[line_type]][node]
                    self.assertEqual(result, test_data)

        result = mod_master_control.master_status()._status_line(0, status['rpi0'])
        self.assertEqual(result, "Errror: Invalid line type")

    def test_mod_master_control_master_status__line(self):
        # Test _line(hostname, data_string)
        module = mod_master_control.master_status()

        data_string = "This is a test string that is very long with line_width = " + str(module.line_width)
        self.assertEqual(module._line("test", data_string), "test: " + data_string)

        data_string = "123456789012345678901234567890"
        module.line_width = 20
        self.assertEqual(module._line("rpi0", data_string), "rpi0:123456789012345")

        data_string = "123456789012345"
        module.line_width = 21
        self.assertEqual(module._line("rpi0", data_string), "rpi0: 123456789012345")

        module.line_width = 20
        self.assertEqual(module._line("rpi0", data_string), "rpi0:123456789012345")
        data_string = "1234567890"
        self.assertEqual(module._line("rpi0", data_string), "rpi0: 1234567890")

        module.line_width = 7
        self.assertEqual(module._line("rpi0", data_string), "rpi0:12")

        module.line_width = 6
        self.assertEqual(module._line("rpi0", data_string), "rpi0:1")

        module.line_width = 5
        self.assertEqual(module._line("rpi0", data_string), "rpi0:")

        module.line_width = 4
        self.assertEqual(module._line("rpi0", data_string), "rpi0")

    def test_mod_master_control_master_status__line_uptime(self):
        # Test _line_uptime(hostname, uptime_str)
        module = mod_master_control.master_status()
        data_string = "123456789012345678901234567890"
        uptime_strings = ["1000d 23h 59m", "364d 23h 59m", "10d 12h 20m", "1d 12h 20m", "10d 12h 20m", "2d 1h 20m", "3d 2h 1m", "12h 10m", "1h 23m", "1h 2m", "12m", "9m"]

        self.assertEqual(module._line_uptime("rpi0", data_string), "rpi0 uptime: " + data_string)
        for uptime in uptime_strings:
            self.assertEqual(module._line_uptime("rpi0", uptime), "rpi0 uptime: " + uptime)

        module.line_width = 100
        self.assertEqual(module._line_uptime("rpi1", data_string), "rpi1 uptime: " + data_string)
        for uptime in uptime_strings:
            self.assertEqual(module._line_uptime("rpi1", uptime), "rpi1 uptime: " + uptime)

        module.line_width = 26
        for uptime in uptime_strings:
            self.assertEqual(module._line_uptime("rpi1", uptime), "rpi1 uptime: " + uptime)

        for uptime in uptime_strings:
            module.line_width = len("rpi1 uptime: ") + len(uptime)
            self.assertEqual(module._line_uptime("rpi1", uptime), "rpi1 uptime: " + uptime)

        for uptime in uptime_strings:
            module.line_width = len("rpi1 uptime:") + len(uptime)
            self.assertEqual(module._line_uptime("rpi1", uptime), "rpi1 uptime:" + uptime)

        for uptime in uptime_strings:
            module.line_width = len("rpi2 up: ") + len(uptime)
            self.assertEqual(module._line_uptime("rpi2", uptime), "rpi2 up: " + uptime)

        for uptime in uptime_strings:
            module.line_width = len("rpi2 up:") + len(uptime)
            self.assertEqual(module._line_uptime("rpi2", uptime), "rpi2 up:" + uptime)

        for uptime in uptime_strings:
            module.line_width = len("rpi2:") + len(uptime)
            self.assertEqual(module._line_uptime("rpi2", uptime), "rpi2:" + uptime)

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_status__os(self, mock_urlopen):
        # Test _os(status)
        module = mod_master_control.master_status()
        test_results_key = 'line_os'

        # Test for bad data
        self.assertEqual(mod_master_control.master_status()._os({}), "Data Error")
        self.assertEqual(mod_master_control.master_status()._os({"hostname":"rpi2"}), "rpi2: Data Error")

        for node in CONFIG.API_HOSTS:
            # Test node at various lengths [-1, 40, 20, 16]
            status = mod_master_control.master_status().get_status(node)
            for line_width in service_master_api_testdata.test_results['status_lines']:
                result = mod_master_control.master_status(line_width)._os(status[node])
                self.assertEqual(result, service_master_api_testdata.test_results['status_lines'][line_width][test_results_key][node])

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_status__ip(self, mock_urlopen):
        # Test _ip(status)
        module = mod_master_control.master_status()
        test_results_key = 'line_ip'

        # Test for bad data
        self.assertEqual(mod_master_control.master_status()._ip({}), "Data Error")
        self.assertEqual(mod_master_control.master_status()._ip({"hostname":"rpi2"}), "rpi2: Data Error")

        for node in CONFIG.API_HOSTS:
            # Test node at various lengths [-1, 40, 20, 16]
            status = mod_master_control.master_status().get_status(node)
            for line_width in service_master_api_testdata.test_results['status_lines']:
                result = mod_master_control.master_status(line_width)._ip(status[node])
                self.assertEqual(result, service_master_api_testdata.test_results['status_lines'][line_width][test_results_key][node])

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_status__usage(self, mock_urlopen):
        # Test _usage(status)
        module = mod_master_control.master_status()
        test_results_key = 'line_usage'

        # Test for bad data
        self.assertEqual(mod_master_control.master_status()._usage({}), "Data Error")
        self.assertEqual(mod_master_control.master_status()._usage({"hostname":"rpi2"}), "rpi2: Data Error")

        for node in CONFIG.API_HOSTS:
            # Test node at various lengths [-1, 40, 20, 16]
            status = mod_master_control.master_status().get_status(node)
            for line_width in service_master_api_testdata.test_results['status_lines']:
                result = mod_master_control.master_status(line_width)._usage(status[node])
                self.assertEqual(result, service_master_api_testdata.test_results['status_lines'][line_width][test_results_key][node])

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_status__uptime(self, mock_urlopen):
        # Test _uptime(status)
        module = mod_master_control.master_status()
        test_results_key = 'line_uptime'

        # Test for bad data
        self.assertEqual(mod_master_control.master_status()._uptime({}), "Data Error")
        self.assertEqual(mod_master_control.master_status()._uptime({"hostname":"rpi2"}), "rpi2: Data Error")

        for node in CONFIG.API_HOSTS:
            # Test node at various lengths [-1, 40, 20, 16]
            status = mod_master_control.master_status().get_status(node)
            for line_width in service_master_api_testdata.test_results['status_lines']:
                result = mod_master_control.master_status(line_width)._uptime(status[node])
                self.assertEqual(result, service_master_api_testdata.test_results['status_lines'][line_width][test_results_key][node])

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_status_shutdown(self, mock_urlopen):
        result = mod_master_control.master_status().shutdown()
        self.assertEqual(result, service_master_api_testdata.test_results['shutdown'])
        result = mod_master_control.master_status().shutdown('rpi0')
        self.assertEqual(result, {'rpi0': service_master_api_testdata.test_results['shutdown']['rpi0']})

        with self.assertRaises(TypeError):
            result = mod_master_control.master_status().shutdown(1)
        with self.assertRaises(KeyError):
            result = mod_master_control.master_status().shutdown("abc")

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_status_reboot(self, mock_urlopen):
        result = mod_master_control.master_status().reboot()
        self.assertEqual(result, service_master_api_testdata.test_results['reboot'])
        result = mod_master_control.master_status().reboot('rpi3')
        self.assertEqual(result, {'rpi3': service_master_api_testdata.test_results['reboot']['rpi3']})

        with self.assertRaises(TypeError):
            result = mod_master_control.master_status().reboot(1)
        with self.assertRaises(KeyError):
            result = mod_master_control.master_status().reboot("abc")

    def test_mod_master_control_master_led_get_settings(self):
        test_settings = self.master_led_default_settings

        module = mod_master_control.master_led()
        self.assertEqual(module.get_settings(), test_settings)

        test_settings["led_mode"] = "auto"
        self.assertNotEqual(module.get_settings(), test_settings)
        module.led_mode = "auto"
        self.assertEqual(module.get_settings(), test_settings)

        test_settings["led_state"] = "002"
        self.assertNotEqual(module.get_settings(), test_settings)
        module.led_state = "002"
        self.assertEqual(module.get_settings(), test_settings)

        test_settings["led_pattern"] = "blink"
        self.assertNotEqual(module.get_settings(), test_settings)
        module.led_pattern = "blink"
        self.assertEqual(module.get_settings(), test_settings)

        test_settings["led_pattern_speed"] = 2
        self.assertNotEqual(module.get_settings(), test_settings)
        module.led_pattern_speed = 2
        self.assertEqual(module.get_settings(), test_settings)


    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_led_get_state(self, mock_urlopen):
        from copy import deepcopy
        test_results = deepcopy(service_master_api_testdata.test_results['get_state'])
        state = mod_master_control.master_led().get_state()
        self.assertEqual(state, test_results)

        del test_results['nodes']['rpi1']
        del test_results['nodes']['rpi2']
        del test_results['nodes']['rpi3']
        state = mod_master_control.master_led().get_state("rpi0")
        self.assertEqual(state, test_results)

        with self.assertRaises(KeyError):
            state = mod_master_control.master_led().get_state("abc")

    @patch('mod_master_control.urlopen', side_effect = mock_call_urlopen)
    def test_mod_master_control_master_led_set_state(self, mock_urlopen):
        from copy import deepcopy
        test_results = deepcopy(service_master_api_testdata.test_results['get_state'])
        test_results['led_state'] = '001'
        test_results['nodes']['rpi0']['state'] = '001'
        test_results['nodes']['rpi1']['state'] = '001'
        test_results['nodes']['rpi2']['state'] = '001'
        test_results['nodes']['rpi3']['state'] = '001'
        state = mod_master_control.master_led().set_state("001")
        self.assertEqual(state, test_results)

        del test_results['nodes']['rpi1']
        del test_results['nodes']['rpi2']
        del test_results['nodes']['rpi3']
        test_results['led_state']='000'
        test_results['nodes']['rpi0']['state'] = '000'
        state = mod_master_control.master_led().set_state("000", "rpi0")
        self.assertEqual(state, test_results)

        with self.assertRaises(ValueError):
            state = mod_master_control.master_led().set_state("abc")
        with self.assertRaises(ValueError):
            state = mod_master_control.master_led().set_state("abc", "rpi1")
        with self.assertRaises(ValueError):
            state = mod_master_control.master_led().set_state("")
        with self.assertRaises(ValueError):
            state = mod_master_control.master_led().set_state("1000")
        with self.assertRaises(KeyError):
            state = mod_master_control.master_led().set_state("000", "abc")

    def test_mod_master_control_master_led_set_mode(self):
        test_settings = self.master_led_default_settings
        module = mod_master_control.master_led()
        test_settings["led_mode"] = "auto"
        self.assertEqual(module.set_mode("auto"), test_settings)

    def test_mod_master_control_master_led_set_pattern(self):
        test_settings = self.master_led_default_settings
        module = mod_master_control.master_led()
        test_settings["led_mode"] = "pattern"
        test_settings["led_pattern"] = "blink"
        self.assertEqual(module.set_pattern("blink"), test_settings)

        test_settings["led_pattern_speed"] = 2
        self.assertEqual(module.set_pattern("blink", 2), test_settings)

        test_settings["led_pattern"] = "rotate"
        self.assertEqual(module.set_pattern("rotate", -1), test_settings)

        test_settings["led_mode"] = "manual"
        test_settings["led_pattern"] = "solid"
        test_settings["led_pattern_speed"] = 1
        self.assertEqual(module.set_pattern("", 0), test_settings)

if __name__ == '__main__':
    unittest.main()
