#!/usr/bin/env python

import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html
from unittest.mock import patch, call

import sys
sys.path.append("../services/status_led")
from mod_display import led_display

#Get Configuration
try:
    #Test for custom config
    import config_status_led_custom as CONFIG
except:
    #If custom config fails load default
    import config_status_led_default as CONFIG

import imp
try:
    imp.find_module('RPi')
    isRPi = True
except ImportError:
    isRPi = False


class UnitTests_mod_display(unittest.TestCase):

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
        self.display_module = led_display()
        self.display_module.pinstates = [ False, False, False ]
        from mod_state_file import state_file
        state_file().write('000')
        self.display_module.blink_delay = CONFIG.BLINK_DELAY

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass


    def test_status_led_mod_display(self):
        self.assertEqual(self.display_module.RED_IDX, 0)
        self.assertEqual(self.display_module.GREEN_IDX, 1)
        self.assertEqual(self.display_module.BLUE_IDX, 2)
        self.assertEqual(self.display_module.pins, [ CONFIG.RED_PIN, CONFIG.GREEN_PIN, CONFIG.BLUE_PIN ])
        self.assertEqual(self.display_module.pinstates, [ False, False, False ])
        self.assertEqual(self.display_module.blink_delay, CONFIG.BLINK_DELAY)

    # =========================================================================
    # Tests for service.status_led.service_display
    # =========================================================================
    @unittest.skipUnless(isRPi, "GPIO required. RPi module not installed.")
    def test_status_led_mod_display_private_on(self):
        # TODO: Add RPi Tests here.
        pass

    @unittest.skipUnless(isRPi, "GPIO required. RPi module not installed.")
    def test_status_led_mod_display_private_off(self):
        # TODO: Add RPi Tests here.
        pass

    def test_status_led_mod_display_on(self):
        self.assertEqual(self.display_module.pinstates, [False, False, False])

        # mock the led_display._on method call.
        with patch.object(led_display,'_on', return_value = True) as mocked_on:
            self.display_module.on(0)
            self.assertEqual(self.display_module.pinstates, [True, False, False])
            self.display_module.on(1)
            self.assertEqual(self.display_module.pinstates, [True, True, False])
            self.display_module.on(2)
            self.assertEqual(self.display_module.pinstates, [True, True, True])

            with self.assertRaises(IndexError):
                self.display_module.on(3)

            with self.assertRaises(IndexError):
                self.display_module.on(-1)

            with self.assertRaises(TypeError):
                self.display_module.on('Red')

    def test_status_led_mod_display_off(self):
        self.display_module.pinstates = [True, True, True]

        # mock the led_display._off method call.
        with patch.object(led_display,'_off', return_value = True) as mocked_off:
            self.assertEqual(self.display_module.pinstates, [True, True, True])
            self.display_module.off(0)
            self.assertEqual(self.display_module.pinstates, [False, True, True])
            self.display_module.off(1)
            self.assertEqual(self.display_module.pinstates, [False, False, True])
            self.display_module.off(2)
            self.assertEqual(self.display_module.pinstates, [False, False, False])

            with self.assertRaises(IndexError):
                self.display_module.off(3)

            with self.assertRaises(IndexError):
                self.display_module.off(-1)

            with self.assertRaises(TypeError):
                self.display_module.off('Red')

    def test_status_led_mod_display_toggle(self):
        # mock the led_display._on method call.
        with patch.object(led_display,'_on', return_value = True) as mocked_on:
            # mock the led_display._off method call.
            with patch.object(led_display,'_off', return_value = True) as mocked_off:
                self.display_module.toggle(0)
                self.assertEqual(self.display_module.pinstates, [True, False, False])
                self.display_module.toggle(0)
                self.display_module.toggle(1)
                self.display_module.toggle(2)
                self.assertEqual(self.display_module.pinstates, [False, True, True])
                self.display_module.toggle(0)
                self.assertEqual(self.display_module.pinstates, [True, True, True])

                with self.assertRaises(IndexError):
                    self.display_module.toggle(3)

                with self.assertRaises(IndexError):
                    self.display_module.toggle(-1)

                with self.assertRaises(TypeError):
                    self.display_module.toggle('Red')

    def test_status_led_mod_display_set_blink_delay(self):
        self.display_module.set_blink_delay(1)
        self.assertEqual(self.display_module.blink_delay, 1)
        self.display_module.set_blink_delay(0.25)
        self.assertEqual(self.display_module.blink_delay, 0.25)
        self.display_module.set_blink_delay(1000)
        self.assertEqual(self.display_module.blink_delay, 1000)
        with self.assertRaises(TypeError):
            self.display_module.set_blink_delay(-1)
        with self.assertRaises(TypeError):
            self.display_module.set_blink_delay(-0.01)
        with self.assertRaises(TypeError):
            self.display_module.set_blink_delay("abc")
        #with self.assertRaises(TypeError):
        #    self.display_module.set_blink_delay(0)

    def test_status_led_mod_display_setpin(self):
        # mock the led_display._on method call.
        with patch.object(led_display,'_on', return_value = True) as mocked_on:
            # mock the led_display._off method call.
            with patch.object(led_display,'_off', return_value = True) as mocked_off:
                self.display_module.setpin(0, 1)
                self.assertEqual(self.display_module.pinstates, [True, False, False])
                self.display_module.setpin(0, 2)
                self.assertEqual(self.display_module.pinstates, [False, False, False])
                self.display_module.setpin(1, 2)
                self.assertEqual(self.display_module.pinstates, [False, True, False])
                self.display_module.setpin(1, 0)
                self.assertEqual(self.display_module.pinstates, [False, False, False])
                self.display_module.setpin(2, 0)
                self.assertEqual(self.display_module.pinstates, [False, False, False])
                self.display_module.setpin(2, 1)
                self.assertEqual(self.display_module.pinstates, [False, False, True])

                with self.assertRaises(IndexError):
                    self.display_module.setpin(3, 0)
                with self.assertRaises(IndexError):
                    self.display_module.setpin(-1, 0)
                with self.assertRaises(TypeError):
                    self.display_module.setpin('Red', 0)

                with self.assertRaises(ValueError):
                    self.display_module.setpin(0, "")
                with self.assertRaises(ValueError):
                    self.display_module.setpin(0, "a")
                with self.assertRaises(ValueError):
                    self.display_module.setpin(0, -1)
                with self.assertRaises(ValueError):
                    self.display_module.setpin(0, 3)

    def test_status_led_mod_display_setpins(self):
        # mock the led_display._on method call.
        with patch.object(led_display,'_on', return_value = True) as mocked_on:
            # mock the led_display._off method call.
            with patch.object(led_display,'_off', return_value = True) as mocked_off:
                self.display_module.setpins("001")
                self.assertEqual(self.display_module.pinstates, [False, False, True])
                self.display_module.setpins("122")
                self.assertEqual(self.display_module.pinstates, [True, True, False])
                self.display_module.setpins("111")
                self.assertEqual(self.display_module.pinstates, [True, True, True])
                self.display_module.setpins("000")
                self.assertEqual(self.display_module.pinstates, [False, False, False])
                self.display_module.setpins("222")
                self.assertEqual(self.display_module.pinstates, [True, True, True])

                with self.assertRaises(ValueError):
                    self.display_module.setpins("")
                with self.assertRaises(ValueError):
                    self.display_module.setpins("10")
                with self.assertRaises(ValueError):
                    self.display_module.setpins("1000")
                with self.assertRaises(ValueError):
                    self.display_module.setpins("-10")
                with self.assertRaises(ValueError):
                    self.display_module.setpins("300")
                with self.assertRaises(ValueError):
                    self.display_module.setpins("abc")
                with self.assertRaises(ValueError):
                    self.display_module.setpins("abc")

    def test_status_led_mod_display_set_exit(self):
        self.assertTrue(self.display_module.set_exit())
        from mod_state_file import state_file
        self.assertEqual(state_file().read(), 'exi')

    def test_status_led_mod_display_display(self):
        # mock the led_display._on method call.
        with patch.object(led_display,'_on', return_value = True) as mocked_on:
            # mock the led_display._off method call.
            with patch.object(led_display,'_off', return_value = True) as mocked_off:
                self.assertTrue(self.display_module.display())
                self.display_module.set_exit()
                self.assertFalse(self.display_module.display())

if __name__ == '__main__':
    unittest.main()
