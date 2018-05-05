#!/usr/bin/env python
# pylint: disable=line-too-long
'''
Tests for Display Service
'''

import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html

#@patch("RPi.GPIO.output", autospec=True)
class UnitTestsServiceDisplay(unittest.TestCase):
    '''
    Test Display Service
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
        pass

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass

    # =========================================================================
    # Tests for service.status_led.service_display
    # =========================================================================
    @unittest.skip('Tests not needed. Coverage in "mod_display_ut.py"')
    def test_status_led_service_display(self):
        '''
        Test the display service function.
        '''
        pass

if __name__ == '__main__':
    unittest.main()
