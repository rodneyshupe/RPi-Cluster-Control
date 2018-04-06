#!/usr/bin/env python

import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html
from unittest.mock import patch

import sys
sys.path.append("../services/status")
import mod_status_info

class UnitTests_mod_status_info(unittest.TestCase):

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
        pass

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass

    # =========================================================================
    # Tests for service.status.mod_status_info
    # =========================================================================
    def test_status_mod_status_info_get_uptime(self):
        with patch('mod_status_info.subprocess.check_output') as mocked_check_output:
            mocked_check_output.return_value = str.encode(' 10:56:20 up 3 days, 10:07,  1 user,  load average: 4.26, 2.84, 2.12')
            uptime = mod_status_info.status_info().get_uptime()
            mocked_check_output.assert_called_with("uptime")
            self.assertEqual(uptime, "3d 10h 07m")

            mocked_check_output.return_value = str.encode(' 21:59:11 up  1:33,  1 user,  load average: 0.02, 0.09, 0.09')
            uptime = mod_status_info.status_info().get_uptime()
            mocked_check_output.assert_called_with("uptime")
            self.assertEqual(uptime, "1h 33m")

            mocked_check_output.return_value = str.encode(' 20:26:06 up 0 min,  1 user,  load average: 0.24, 0.06, 0.02')
            uptime = mod_status_info.status_info().get_uptime()
            mocked_check_output.assert_called_with("uptime")
            self.assertEqual(uptime, "0m")

            mocked_check_output.return_value = str.encode(' 20:26:06 up 10 min,  1 user,  load average: 0.24, 0.06, 0.02')
            uptime = mod_status_info.status_info().get_uptime()
            mocked_check_output.assert_called_with("uptime")
            self.assertEqual(uptime, "10m")

    def test_status_mod_status_info_get_cpu_temperature(self):
        with patch('mod_status_info.subprocess.check_output') as mocked_check_output:
            mocked_check_output.return_value = str.encode('temp=54.8\'C')
            temp = mod_status_info.status_info().get_cpu_temperature()
            mocked_check_output.assert_called_with(['vcgencmd', 'measure_temp'])
            self.assertIsInstance(temp, (int, float))
            self.assertEqual(temp, 54.8)

    def test_status_mod_status_info_get_ram_info_free(self):
        self.assertIsInstance(mod_status_info.status_info().get_ram_info(), dict)
        with patch('mod_status_info.subprocess.check_output') as mocked_check_output:
            mocked_check_output.return_value = str.encode('              total        used        free      shared  buff/cache   available\nMem:        1000312      490444       35076       56956      474792      393872\nSwap:             0           0           0\n')
            get_ram_info = mod_status_info.status_info().get_ram_info()
            mocked_check_output.assert_called_with('free')
            self.assertIsInstance(get_ram_info, dict)
            self.assertEqual(get_ram_info, {'method':'free', 'total': 1000312, 'free': 35076, 'used': 490444, 'percent_used': 49.0})

    def test_status_mod_status_info_get_ram_info_psutil(self):
        with patch('mod_status_info.subprocess.check_output') as mocked_check_output:
            mocked_check_output.return_value = ''

            with patch('psutil.virtual_memory') as mocked_virtual_memory:
                mocked_virtual_memory.return_value = [8589934592, 1734578176, 79.8, 7454433280, 334585856, 1619017728, 1399992320, 4435423232]
                get_ram_info = mod_status_info.status_info().get_ram_info()
                mocked_check_output.assert_called_with('free')
                self.assertIsInstance(get_ram_info, dict)
                self.assertEqual(get_ram_info, {'method':'psutil', 'total': 8589934592, 'used': 7454433280, 'free': 1734578176, 'percent_used': 79.8})

                mocked_virtual_memory.return_value = [8000000000, 2000000000, 75.0, 6000000000, 300000000, 1619017728, 1399992320, 4435423232]
                get_ram_info = mod_status_info.status_info().get_ram_info()
                mocked_check_output.assert_called_with('free')
                self.assertIsInstance(get_ram_info, dict)
                self.assertEqual(get_ram_info, {'method':'psutil', 'total': 8000000000, 'used': 6000000000, 'free': 2000000000, 'percent_used': 75.0})

    def test_status_mod_status_info_get_ram_info_nofree_nopsutil(self):
        with patch('mod_status_info.subprocess.check_output') as mocked_check_output:
            mocked_check_output.return_value = ''

            with patch('psutil.virtual_memory') as mocked_virtual_memory:
                mocked_virtual_memory.return_value = []
                get_ram_info = mod_status_info.status_info().get_ram_info()
                mocked_check_output.assert_called_with('free')
                self.assertIsInstance(get_ram_info, dict)
                self.assertEqual(get_ram_info, {'method':'n/a', 'total': None, 'used': None, 'free': None, 'percent_used': None})

    def test_status_mod_status_info_get_ram_percent(self):
        with patch('mod_status_info.subprocess.check_output') as mocked_check_output:
            mocked_check_output.return_value = str.encode('              total        used        free      shared  buff/cache   available\nMem:        1000312      490444       35076       56956      474792      393872\nSwap:             0           0           0\n')
            get_ram_percent = mod_status_info.status_info().get_ram_percent()
            mocked_check_output.assert_called_with('free')
            self.assertIsInstance(get_ram_percent, float)
            self.assertEqual(get_ram_percent, 49.0)

    def test_status_mod_status_info_get_cpu_usage(self):
        self.assertIsInstance(mod_status_info.status_info().get_cpu_usage(), (int, float))

        with patch('mod_status_info.psutil.cpu_percent') as mocked_cpu_percent:
            mocked_cpu_percent.return_value = 20.5
            get_cpu_percent = mod_status_info.status_info().get_cpu_usage()
            self.assertEqual(get_cpu_percent, 20.5)

    def test_status_mod_status_info_get_hostname(self):
        with patch('mod_status_info.socket.getfqdn') as mocked_getfqdn:
            mocked_getfqdn.return_value = 'rodney-mac-wifi.lan\nrodney-mac-wifi.lan\nok\n'
            get_hostname = mod_status_info.status_info().get_hostname()
            self.assertEqual(get_hostname, 'rodn')

            mocked_getfqdn.return_value = 'rpi0'
            get_hostname = mod_status_info.status_info().get_hostname()
            self.assertEqual(get_hostname, 'rpi0')

    def test_status_mod_status_info_get_ip_address(self):
        with patch('mod_status_info.socket.socket.getsockname') as mocked_getsockname:
            mocked_getsockname.return_value = ['192.168.8.100', 35527]
            get_hostname = mod_status_info.status_info().get_ip_address()
            self.assertEqual(get_hostname, '192.168.8.100')

            mocked_getsockname.return_value = ['192.168.1.100']
            get_hostname = mod_status_info.status_info().get_ip_address()
            self.assertEqual(get_hostname, '192.168.1.100')

    def test_status_mod_status_info_get_debug_info(self):
        debug_info = mod_status_info.status_info().get_debug_info()
        self.assertIsInstance(debug_info, dict)
        self.assertIsInstance(debug_info['python_vesion'], str)
        self.assertIsInstance(debug_info['psutil_version'], str)

        # TODO Add Test to make sure all elements are returned.

    def test_status_mod_status_info_get_uname(self):
        with patch('mod_status_info.platform.uname') as mocked_uname:
            mocked_uname.return_value = ['Linux', 'rpi0', '4.9.80-v7+', '#1098 SMP Fri Mar 9 19:11:42 GMT 2018', 'armv7l', '']
            uname = mod_status_info.status_info().get_uname()
            self.assertEqual(uname, {'node': 'rpi0', 'system': 'Linux', 'machine': 'armv7l', 'version': '#1098 SMP Fri Mar 9 19:11:42 GMT 2018', 'release': '4.9.80-v7+', 'processor': ''})

            mocked_uname.return_value = ['Darwin', 'Rodney-Mac-wifi.lan', '17.4.0', 'Darwin Kernel Version 17.4.0: Sun Dec 17 09:19:54 PST 2017; root:xnu-4570.41.2~1/RELEASE_X86_64', 'x86_64', 'i386']
            uname = mod_status_info.status_info().get_uname()
            self.assertEqual(uname, {'node': 'Rodney-Mac-wifi.lan', 'system': 'Darwin', 'machine': 'x86_64', 'version': 'Darwin Kernel Version 17.4.0: Sun Dec 17 09:19:54 PST 2017; root:xnu-4570.41.2~1/RELEASE_X86_64', 'release': '17.4.0', 'processor': 'i386'})

    def test_status_mod_status_info_get_info(self):
        info_default = mod_status_info.status_info().get_info()
        info_with_false = mod_status_info.status_info().get_info(False)
        info_with_true = mod_status_info.status_info().get_info(True)

        self.assertTrue(info_default['hostname'])
        self.assertTrue(info_default['ip'])
        self.assertTrue(info_default['uptime'])
        self.assertTrue(info_default['cpu'])
        self.assertTrue(info_default['cpu']['temperature'])
        self.assertTrue('usage' in info_default['cpu'])
        self.assertTrue(info_default['cpu_count'])
        self.assertTrue(info_default['uname'])
        self.assertTrue(info_default['ram'])
        self.assertFalse(contains_key(info_default, 'debug'))

        self.assertTrue(info_with_false['hostname'])
        self.assertTrue(info_with_false['ip'])
        self.assertTrue(info_with_false['uptime'])
        self.assertTrue(info_with_false['cpu'])
        self.assertTrue(info_with_false['cpu']['temperature'])
        self.assertTrue('usage' in info_with_false['cpu'])
        self.assertTrue(info_with_false['cpu_count'])
        self.assertTrue(info_with_false['uname'])
        self.assertTrue(info_with_false['ram'])
        self.assertFalse(contains_key(info_with_false, 'debug'))

        self.assertTrue(info_with_true['hostname'])
        self.assertTrue(info_with_true['ip'])
        self.assertTrue(info_with_true['uptime'])
        self.assertTrue(info_with_true['cpu'])
        self.assertTrue(info_with_true['cpu']['temperature'])
        self.assertTrue('usage' in info_with_true['cpu'])
        self.assertTrue(info_with_true['cpu_count'])
        self.assertTrue(info_with_true['uname'])
        self.assertTrue(info_with_true['ram'])
        self.assertTrue(info_with_true['debug'])

if __name__ == '__main__':
    unittest.main()

def contains_key(dictionary, key):
    try:
        test = dictionary[key]
        return(True)
    except KeyError as e:
        #test = "Missing key '{0}' in the response data".format(str(e))
        return(False)
    return(None)
