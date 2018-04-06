#!/usr/bin/env python

import sys
sys.path.append("../services/status_led")
import service_state_api
import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html
import json
import mod_state_file

class UnitTests_service_state_api(unittest.TestCase):

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
        # Setup state file into known quanity
        self.original_state = mod_state_file.state_file().read()
        mod_state_file.state_file().init("000")

        # creates a test client
        self.app = service_state_api.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        service_state_api.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        # Reset state
        mod_state_file.state_file().write(self.original_state)


    # =========================================================================
    # Tests for service.status_led.service_status_api
    # =========================================================================
    def test_status_led_service_status_api_get_state(self):
        result = self.app.get('/api/v1.0/state')
        self.assertEqual(result.status_code, 200)
        state = json.loads(result.data)
        self.assertEqual(state, {'state': '000'})

        mod_state_file.state_file().write('020')
        result = self.app.get('/api/v1.0/state')
        self.assertEqual(result.status_code, 200)
        state = json.loads(result.data)
        self.assertEqual(state, {'state': '020'})


    def test_status_led_service_status_api_set_state(self):
        result = self.app.get('/api/v1.0/state/001')
        self.assertEqual(result.status_code, 200)
        state = json.loads(result.data)
        self.assertEqual(state, {'state': '001'})
        self.assertEqual(mod_state_file.state_file().read(), '001')

        result = self.app.get('/api/v1.0/state/020')
        self.assertEqual(result.status_code, 200)
        state = json.loads(result.data)
        self.assertEqual(state, {'state': '020'})
        self.assertEqual(mod_state_file.state_file().read(), '020')

        result = self.app.get('/api/v1.0/state/abc')
        self.assertEqual(result.status_code, 200)
        state = json.loads(result.data)
        self.assertEqual(state, {'state': '020', 'error': 'Invalid Value: "abc" State must be 3 digits.'})
        self.assertEqual(mod_state_file.state_file().read(), '020')

if __name__ == '__main__':
    unittest.main()
