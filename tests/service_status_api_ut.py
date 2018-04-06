#!/usr/bin/env python

import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html
from unittest.mock import patch

import sys
sys.path.append("../services/status")
import service_status_api
import mod_status_info

import json

def dictionarys_equal(dict1, dict2):
    return_value = True
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        for keys in set(dict1) & set(dict2):
            if (keys in dict1) and (keys in dict2):
                if isinstance(dict1[keys], dict):
                    return_value = return_value and dictionarys_equal(dict1[keys], dict2[keys])
            else:
                return_value = False
    else:
        return_value = False
    return(return_value)

class UnitTests_service_status_api(unittest.TestCase):

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
        # creates a test client
        self.app = service_status_api.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        service_status_api.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        self.maxDiff = None

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass

    # =========================================================================
    # Tests for service.status_led.service_status_api
    # =========================================================================
    def test_service_status_api_do_shutdown(self):
        shutdown_response = {"action":"Shutdown", "command":"/usr/bin/sudo /sbin/shutdown now", "result":"ok"}
        reboot_response = {"action":"Reboot", "command":"/usr/bin/sudo /sbin/shutdown -r now", "result":"ok"}
        with patch('subprocess.Popen') as mocked_check_output:
            mocked_check_output.return_value.communicate.return_value = ["ok"]
            result = service_status_api.do_shutdown()
            self.assertEqual(result, shutdown_response)
            result = service_status_api.do_shutdown(True)
            self.assertEqual(result, reboot_response)
            result = service_status_api.do_shutdown(False)
            self.assertEqual(result, shutdown_response)

    def test_service_status_api_status(self):
        result = self.app.get('/api/v1.0/status') # service_status_api.do_status()
        self.assertEqual(result.status_code, 200)
        status = json.loads(result.data)
        test_results = mod_status_info.status_info().get_info()
        self.assertTrue(dictionarys_equal(status, test_results))

    def test_service_status_api_status_debug(self):
        result = self.app.get('/api/v1.0/status/debug') # service_status_api.do_status()
        self.assertEqual(result.status_code, 200)
        status = json.loads(result.data)
        test_results = mod_status_info.status_info().get_info(True)
        self.assertTrue(dictionarys_equal(status, test_results))

    def test_service_status_api_debug(self):
        result = self.app.get('/api/v1.0/debug') # service_status_api.do_status()
        self.assertEqual(result.status_code, 200)
        status = json.loads(result.data)
        test_results = mod_status_info.status_info().get_debug_info()
        self.assertTrue(dictionarys_equal(status, test_results))

    def test_service_status_api_shutdown(self):
        standard_response = {"action":"Shutdown", "command":"/usr/bin/sudo /sbin/shutdown now", "result":"ok"}
        with patch('subprocess.Popen') as mocked_check_output:
            mocked_check_output.return_value.communicate.return_value = ["ok"]
            result = self.app.get('/api/v1.0/shutdown')
            self.assertEqual(result.status_code, 200)
            response = json.loads(result.data)
            self.assertEqual(response, standard_response)

    def test_service_status_api_reboot(self):
        standard_response = {"action":"Reboot", "command":"/usr/bin/sudo /sbin/shutdown -r now", "result":"ok"}
        with patch('subprocess.Popen') as mocked_check_output:
            mocked_check_output.return_value.communicate.return_value = ["ok"]
            result = self.app.get('/api/v1.0/shutdown/reboot')
            self.assertEqual(result.status_code, 200)
            response = json.loads(result.data)
            self.assertEqual(response, standard_response)

if __name__ == '__main__':
    unittest.main()
