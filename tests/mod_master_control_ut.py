#!/usr/bin/env python
# pylint: disable=line-too-long
""" Unit Tests for mod_display """

import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html
from unittest.mock import patch, Mock

import urllib.request

#pylint: disable=wrong-import-position
import sys
sys.path.append("../services/master")
import mod_master_control # pylint: disable=E0401
import config_master_default as CONFIG # pylint: disable=E0401
#pylint: enable=wrong-import-position

#Build testdata
import service_master_api_testdata
import service_status_api_testdata
import service_state_api_testdata
TESTDATA = {}
for key in service_status_api_testdata.TESTDATA:
    TESTDATA[key] = service_status_api_testdata.TESTDATA[key]
for key in service_state_api_testdata.TESTDATA:
    TESTDATA[key] = service_state_api_testdata.TESTDATA[key]

# pylint: disable=C0301
# pylint: disable=R0914
# pylint: disable=R0904
class UnitTestsModMasterControl(unittest.TestCase):
    '''
    Tests for mod_master_control.py
    '''

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
        self.maxDiff = None # pylint: disable=invalid-name

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass

    # These function used used to mock the urlib.request.urlopen method
    # pylint: disable=E0213
    def mock_call_urlopen(request_obj): # pylint: disable=W0613
        '''
        Simulate URL Open
        '''
        with patch('urllib.request.urlopen') as mocked_urlopen:
            mock_urlopen_return = Mock()
            url = request_obj._full_url # pylint: disable=E1101
            try:
                return_value = TESTDATA[url]
            except KeyError:
                return_value = '{"error":"No test data for ' + url + '"}'
                raise ValueError('No test data for ' + url)

            mock_urlopen_return.read.return_value = return_value
            mocked_urlopen.return_value = mock_urlopen_return
            #request = Request(url, method='GET')
            result = urllib.request.urlopen(request_obj)
        return result
    # pylint: enable=E0213

    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_host_method(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test mod_master_control.host_method(method, node=None, protocol='GET')
        '''
        mod_master_control.CONFIG.USE_MULTITREADING = False

        result = mod_master_control.host_method(method=':5002/api/v1.0/status', protocol="GET")
        test_result = service_master_api_testdata.TEST_RESULTS['get_status']
        self.assertEqual(result, test_result)

        result = mod_master_control.host_method(method=':5002/api/v1.0/status', node="rpi1", protocol="GET")
        test_result = {'rpi1':service_master_api_testdata.TEST_RESULTS['get_status']['rpi1']}
        self.assertEqual(result, test_result)

        mod_master_control.CONFIG.USE_MULTITREADING = True

        result = mod_master_control.host_method(method=':5002/api/v1.0/status', protocol="GET")
        test_result = service_master_api_testdata.TEST_RESULTS['get_status']
        self.assertEqual(result, test_result)

        result = mod_master_control.host_method(method=':5002/api/v1.0/status', node="rpi2", protocol="GET")
        test_result = {'rpi2':service_master_api_testdata.TEST_RESULTS['get_status']['rpi2']}
        self.assertEqual(result, test_result)

        #ValueError
        with self.assertRaises(ValueError):
            mod_master_control.host_method(method='')
        with self.assertRaises(ValueError):
            mod_master_control.host_method(method='', node='', protocol="GET")

    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_host_call(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test mod_master_control.host_call
        '''
        with self.assertRaises(Exception):
            mod_master_control.host_method(method='')

    def test_master_status_get_hosts(self):
        '''
        Test Get Hosts
        '''
        hosts = mod_master_control.MasterStatus().get_hosts()
        self.assertEqual(hosts, mod_master_control.CONFIG.API_HOSTS)

    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_master_status_get_status(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test get_status(node = "", debug=False)
        '''
        status = mod_master_control.MasterStatus().get_status()
        self.assertEqual(status, service_master_api_testdata.TEST_RESULTS['get_status'])

        status = mod_master_control.MasterStatus().get_status("rpi0")
        test_result = {'rpi0': service_master_api_testdata.TEST_RESULTS['get_status']['rpi0']}
        self.assertEqual(status, test_result)

        with self.assertRaises(KeyError):
            status = mod_master_control.MasterStatus().get_status(1)
        with self.assertRaises(KeyError):
            status = mod_master_control.MasterStatus().get_status("abc")

    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_get_status_line(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test get_status_line(line_types = [1, 2, 3, 4], node = "", line_width = -1)
        '''
        #status = mod_master_control.MasterStatus().get_status()
        line_types_list = [[2, 3], [1, 2, 3, 4], 2]
        line_type_keys = {4: 'line_os', 3: 'line_ip', 1: 'line_usage', 2: 'line_uptime'}

        # Test all passed in
        for line_types in line_types_list:
            # Test multiple nodes at various lengths [-1, 40, 20, 16]
            for node in CONFIG.API_HOSTS:
                # Test node at various lengths [-1, 40, 20, 16]
                for line_width in service_master_api_testdata.TEST_RESULTS['status_lines']:
                    mod_master_status = mod_master_control.MasterStatus(line_width)
                    result = mod_master_status.get_status_line(line_types, node, line_width)
                    test_data = {}
                    if isinstance(line_types, list):
                        lines_types_for_loop = line_types
                    else:
                        lines_types_for_loop = [line_types]
                    for line_type in lines_types_for_loop:
                        lines = service_master_api_testdata.TEST_RESULTS['status_lines']
                        data = lines[line_width][line_type_keys[line_type]][node]
                        node_data = data

                        test_data[line_type] = {node : node_data}
                    self.assertEqual(result, test_data)

        # Test no node passed
        for line_types in line_types_list:
            # Test multiple nodes at various lengths [-1, 40, 20, 16]
            for line_width in service_master_api_testdata.TEST_RESULTS['status_lines']:
                master_status = mod_master_control.MasterStatus(line_width)
                lines = master_status.get_status_line(line_types=line_types, line_width=line_width)
                result = lines
                test_data = {}
                if isinstance(line_types, list):
                    lines_types_for_loop = line_types
                else:
                    lines_types_for_loop = [line_types]
                for line_type in lines_types_for_loop:
                    test_data[line_type] = {}
                    for node in CONFIG.API_HOSTS:
                        lines = service_master_api_testdata.TEST_RESULTS['status_lines']
                        data = lines[line_width][line_type_keys[line_type]][node]
                        test_data[line_type][node] = data
                self.assertEqual(result, test_data)

    # pylint: disable=W0212
    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_master_status__status_line(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test _status_line(line_type, status)
        '''
        line_types = {4: 'line_os', 3: 'line_ip', 1: 'line_usage', 2: 'line_uptime'}

        status = mod_master_control.MasterStatus().get_status()
        for line_type in range(1, 4):
            # Test multiple nodes at various lengths [-1, 40, 20, 16]
            for node in CONFIG.API_HOSTS:
                # Test node at various lengths [-1, 40, 20, 16]
                for line_width in service_master_api_testdata.TEST_RESULTS['status_lines']:
                    result = mod_master_control.MasterStatus(line_width)._status_line(line_type, status[node])
                    test_data = service_master_api_testdata.TEST_RESULTS['status_lines'][line_width][line_types[line_type]][node]
                    self.assertEqual(result, test_data)

        result = mod_master_control.MasterStatus()._status_line(0, status['rpi0'])
        self.assertEqual(result, "Errror: Invalid line type")
    # pylint: enable=W0212

    # pylint: disable=W0212
    def test_master_status_line(self):
        '''
        Test _line(hostname, data_string)
        '''
        module = mod_master_control.MasterStatus()

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
    # pylint: enable=W0212

    # pylint: disable=W0212
    def test_master_status__line_uptime(self):
        '''
        Test _line_uptime(hostname, uptime_str)
        '''
        module = mod_master_control.MasterStatus()
        data_string = "123456789012345678901234567890"
        uptime_strings = [
            "1000d 23h 59m",
            "364d 23h 59m",
            "10d 12h 20m",
            "1d 12h 20m",
            "10d 12h 20m",
            "2d 1h 20m",
            "3d 2h 1m",
            "12h 10m",
            "1h 23m",
            "1h 2m",
            "12m",
            "9m"]

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
    # pylint: enable=W0212

    # pylint: disable=W0212
    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_master_status__os(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test mod_master_control.MasterStatus()._os(status)
        '''
        #module = mod_master_control.MasterStatus()
        test_results_key = 'line_os'

        # Test for bad data
        self.assertEqual(mod_master_control.MasterStatus()._os({}), "Data Error")
        self.assertEqual(mod_master_control.MasterStatus()._os({"hostname":"rpi2"}), "rpi2: Data Error")

        for node in CONFIG.API_HOSTS:
            # Test node at various lengths [-1, 40, 20, 16]
            status = mod_master_control.MasterStatus().get_status(node)
            for line_width in service_master_api_testdata.TEST_RESULTS['status_lines']:
                result = mod_master_control.MasterStatus(line_width)._os(status[node])
                self.assertEqual(result, service_master_api_testdata.TEST_RESULTS['status_lines'][line_width][test_results_key][node])
    # pylint: enable=W0212

    # pylint: disable=W0212
    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_master_status__ip(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test mod_master_control.MasterStatus()._ip(status)
        '''
        #module = mod_master_control.MasterStatus()
        test_results_key = 'line_ip'

        # Test for bad data
        self.assertEqual(mod_master_control.MasterStatus()._ip({}), "Data Error")
        self.assertEqual(mod_master_control.MasterStatus()._ip({"hostname":"rpi2"}), "rpi2: Data Error")

        for node in CONFIG.API_HOSTS:
            # Test node at various lengths [-1, 40, 20, 16]
            status = mod_master_control.MasterStatus().get_status(node)
            for line_width in service_master_api_testdata.TEST_RESULTS['status_lines']:
                result = mod_master_control.MasterStatus(line_width)._ip(status[node])
                self.assertEqual(result, service_master_api_testdata.TEST_RESULTS['status_lines'][line_width][test_results_key][node])
    # pylint: enable=W0212

    # pylint: disable=W0212
    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_master_status__usage(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test mod_master_control.MasterStatus()._usage(status)
        '''
        test_results_key = 'line_usage'

        # Test for bad data
        self.assertEqual(mod_master_control.MasterStatus()._usage({}), "Data Error")
        self.assertEqual(mod_master_control.MasterStatus()._usage({"hostname":"rpi2"}), "rpi2: Data Error")

        for node in CONFIG.API_HOSTS:
            # Test node at various lengths [-1, 40, 20, 16]
            status = mod_master_control.MasterStatus().get_status(node)
            for line_width in service_master_api_testdata.TEST_RESULTS['status_lines']:
                result = mod_master_control.MasterStatus(line_width)._usage(status[node])
                self.assertEqual(result, service_master_api_testdata.TEST_RESULTS['status_lines'][line_width][test_results_key][node])
    # pylint: enable=W0212

    # pylint: disable=W0212
    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_master_status__uptime(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test mod_master_control.MasterStatus()._uptime(status)
        '''
        test_results_key = 'line_uptime'

        # Test for bad data
        self.assertEqual(mod_master_control.MasterStatus()._uptime({}), "Data Error")
        self.assertEqual(mod_master_control.MasterStatus()._uptime({"hostname":"rpi2"}), "rpi2: Data Error")

        for node in CONFIG.API_HOSTS:
            # Test node at various lengths [-1, 40, 20, 16]
            status = mod_master_control.MasterStatus().get_status(node)
            for line_width in service_master_api_testdata.TEST_RESULTS['status_lines']:
                result = mod_master_control.MasterStatus(line_width)._uptime(status[node])
                self.assertEqual(result, service_master_api_testdata.TEST_RESULTS['status_lines'][line_width][test_results_key][node])
    # pylint: enable=W0212

    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_master_status_shutdown(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test mod_master_control.MasterStatus().shutdown()
        '''
        result = mod_master_control.MasterStatus().shutdown()
        self.assertEqual(result, service_master_api_testdata.TEST_RESULTS['shutdown'])
        result = mod_master_control.MasterStatus().shutdown('rpi0')
        self.assertEqual(result, {'rpi0': service_master_api_testdata.TEST_RESULTS['shutdown']['rpi0']})

        with self.assertRaises(KeyError):
            result = mod_master_control.MasterStatus().shutdown(1)
        with self.assertRaises(KeyError):
            result = mod_master_control.MasterStatus().shutdown("abc")

    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_master_status_reboot(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test mod_master_control.MasterStatus().reboot()
        '''
        result = mod_master_control.MasterStatus().reboot()
        self.assertEqual(result, service_master_api_testdata.TEST_RESULTS['reboot'])
        result = mod_master_control.MasterStatus().reboot('rpi3')
        self.assertEqual(result, {'rpi3': service_master_api_testdata.TEST_RESULTS['reboot']['rpi3']})

        with self.assertRaises(KeyError):
            result = mod_master_control.MasterStatus().reboot(1)
        with self.assertRaises(KeyError):
            result = mod_master_control.MasterStatus().reboot("abc")

    def test_master_led_get_settings(self):
        '''
        Test mod_master_control.MasterLed().get_settings()
        '''
        test_settings = self.master_led_default_settings

        module = mod_master_control.MasterLed()
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


    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_master_led_get_state(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test mod_master_control.MasterLed().get_state()
        '''
        from copy import deepcopy
        test_results = deepcopy(service_master_api_testdata.TEST_RESULTS['get_state'])
        state = mod_master_control.MasterLed().get_state()
        self.assertEqual(state, test_results)

        del test_results['nodes']['rpi1']
        del test_results['nodes']['rpi2']
        del test_results['nodes']['rpi3']
        state = mod_master_control.MasterLed().get_state("rpi0")
        self.assertEqual(state, test_results)

        with self.assertRaises(KeyError):
            state = mod_master_control.MasterLed().get_state("abc")

    @patch('mod_master_control.urlopen', side_effect=mock_call_urlopen)
    def test_master_led_set_state(self, mock_urlopen): # pylint: disable=W0613
        '''
        Test mod_master_control.MasterLed().set_state()
        '''
        from copy import deepcopy
        test_results = deepcopy(service_master_api_testdata.TEST_RESULTS['get_state'])
        test_results['led_state'] = '001'
        test_results['nodes']['rpi0']['state'] = '001'
        test_results['nodes']['rpi1']['state'] = '001'
        test_results['nodes']['rpi2']['state'] = '001'
        test_results['nodes']['rpi3']['state'] = '001'
        state = mod_master_control.MasterLed().set_state("001")
        self.assertEqual(state, test_results)

        del test_results['nodes']['rpi1']
        del test_results['nodes']['rpi2']
        del test_results['nodes']['rpi3']
        test_results['led_state'] = '000'
        test_results['nodes']['rpi0']['state'] = '000'
        state = mod_master_control.MasterLed().set_state("000", "rpi0")
        self.assertEqual(state, test_results)

        with self.assertRaises(ValueError):
            state = mod_master_control.MasterLed().set_state("abc")
        with self.assertRaises(ValueError):
            state = mod_master_control.MasterLed().set_state("abc", "rpi1")
        with self.assertRaises(ValueError):
            state = mod_master_control.MasterLed().set_state("")
        with self.assertRaises(ValueError):
            state = mod_master_control.MasterLed().set_state("1000")
        with self.assertRaises(KeyError):
            state = mod_master_control.MasterLed().set_state("000", "abc")

    def test_master_led_set_mode(self):
        '''
        Test mod_master_control.MasterLed().set_mode()
        '''
        test_settings = self.master_led_default_settings
        module = mod_master_control.MasterLed()
        test_settings["led_mode"] = "auto"
        self.assertEqual(module.set_mode("auto"), test_settings)

    def test_master_led_set_pattern(self):
        '''
        Test mod_master_control.MasterLed().set_pattern()
        '''
        test_settings = self.master_led_default_settings
        module = mod_master_control.MasterLed()
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
