#!/usr/bin/env python

import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html

import sys
sys.path.append("../services/status_led")
import mod_state_file

class UnitTests_mod_state_file(unittest.TestCase):

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
    # Tests for service.status_led.mod_state_file
    # =========================================================================
    def test_mod_state_file_valid_state(self):
        self.assertFalse(mod_state_file.state_file().valid_state(""))
        self.assertFalse(mod_state_file.state_file().valid_state("10"))
        self.assertFalse(mod_state_file.state_file().valid_state("1000"))
        self.assertFalse(mod_state_file.state_file().valid_state("-10"))
        self.assertFalse(mod_state_file.state_file().valid_state("abc"))
        self.assertTrue(mod_state_file.state_file().valid_state("000"))
        self.assertTrue(mod_state_file.state_file().valid_state("111"))
        self.assertTrue(mod_state_file.state_file().valid_state("222"))
        self.assertTrue(mod_state_file.state_file().valid_state("100"))
        self.assertTrue(mod_state_file.state_file().valid_state("010"))
        self.assertTrue(mod_state_file.state_file().valid_state("001"))
        self.assertTrue(mod_state_file.state_file().valid_state("200"))
        self.assertTrue(mod_state_file.state_file().valid_state("020"))
        self.assertTrue(mod_state_file.state_file().valid_state("002"))
        self.assertTrue(mod_state_file.state_file().valid_state("222"))
        self.assertFalse(mod_state_file.state_file().valid_state("223"))
        self.assertFalse(mod_state_file.state_file().valid_state("003"))
        self.assertTrue(mod_state_file.state_file().valid_state("211"))
        self.assertTrue(mod_state_file.state_file().valid_state("121"))
        self.assertTrue(mod_state_file.state_file().valid_state("112"))

    def test_mod_state_file_get_state_file(self):
        import os

        # Prep for tests
        goodpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        goodpath += "/services/status_led/.state"
        try:
            os.remove(goodpath)
        except OSError:
            pass

        # Test state_file():
        badpath = os.path.dirname(os.path.realpath(__file__))
        badpath += "/.state"
        self.assertEqual(mod_state_file.state_file().state_file(), goodpath)
        self.assertNotEqual(mod_state_file.state_file().state_file(), badpath)

    def test_mod_state_file_read_write_exceptions(self):
        # Test Read with No File.
        with self.assertRaises(IOError):
            mod_state_file.state_file().read()

        with self.assertRaises(ValueError):
            mod_state_file.state_file().write("")
        with self.assertRaises(ValueError):
            mod_state_file.state_file().write("10")
        with self.assertRaises(ValueError):
            mod_state_file.state_file().write("1000")
        with self.assertRaises(ValueError):
            mod_state_file.state_file().write("-10")
        with self.assertRaises(ValueError):
            mod_state_file.state_file().write("300")
        with self.assertRaises(ValueError):
            mod_state_file.state_file().write("abc")
        with self.assertRaises(ValueError):
            mod_state_file.state_file().init("abc")

    def test_mod_state_file_read_write_test(self):
        self.assertEqual(mod_state_file.state_file().init(), "000")
        self.assertEqual(mod_state_file.state_file().read(), "000")
        self.assertNotEqual(mod_state_file.state_file().read(), "001")
        self.assertEqual(mod_state_file.state_file().init("010"), "010")
        self.assertNotEqual(mod_state_file.state_file().write("100"), "000")
        self.assertEqual(mod_state_file.state_file().read(), "100")

if __name__ == '__main__':
    unittest.main()
