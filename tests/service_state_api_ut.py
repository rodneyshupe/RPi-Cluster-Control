#!/usr/bin/env python
# pylint: disable=line-too-long
""" Unit Tests for mod_display """

import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html
import json


# pylint: disable=wrong-import-position
import sys
sys.path.append("../services/status_led")
import service_state_api # pylint: disable=import-error
import mod_state_file # pylint: disable=import-error
# pylint: enable=wrong-import-position

class UnitTestsServiceStateApi(unittest.TestCase):
    """
    Class containing unit tests for State API methods
    """

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
        self.original_state = mod_state_file.StateFile().read()
        mod_state_file.StateFile().init("000")

        # creates a test client
        self.app = service_state_api.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        service_state_api.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        # Reset state
        mod_state_file.StateFile().write(self.original_state)


    # =========================================================================
    # Tests for service.status_led.service_status_api
    # =========================================================================
    def test_get_state(self):
        """
        Tests Get State Method
        """
        result = self.app.get('/api/v1.0/state')
        self.assertEqual(result.status_code, 200)
        state = json.loads(result.data)
        self.assertEqual(state, {'state': '000'})

        mod_state_file.StateFile().write('020')
        result = self.app.get('/api/v1.0/state')
        self.assertEqual(result.status_code, 200)
        state = json.loads(result.data)
        self.assertEqual(state, {'state': '020'})


    def test_set_state(self):
        """
        Tests the Set State Method
        """
        result = self.app.get('/api/v1.0/state/001')
        self.assertEqual(result.status_code, 405)

        result = self.app.patch('/api/v1.0/state/001')
        self.assertEqual(result.status_code, 200)

        state = json.loads(result.data)
        self.assertEqual(state, {'state': '001'})
        self.assertEqual(mod_state_file.StateFile().read(), '001')

        result = self.app.patch('/api/v1.0/state/020')
        self.assertEqual(result.status_code, 200)

        state = json.loads(result.data)
        self.assertEqual(state, {'state': '020'})
        self.assertEqual(mod_state_file.StateFile().read(), '020')

        result = self.app.patch('/api/v1.0/state/abc')
        self.assertEqual(result.status_code, 200)
        state = json.loads(result.data)
        test_result = {
            'state': '020',
            'error': 'Invalid Value: "abc" State must be 3 digits.'
        }
        self.assertEqual(state, test_result)
        self.assertEqual(mod_state_file.StateFile().read(), '020')

if __name__ == '__main__':
    unittest.main()
