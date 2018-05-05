#!/usr/bin/env python
# pylint: disable=line-too-long
""" Unit Tests for mod_display """

import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html

#pylint: disable=wrong-import-position
import sys
sys.path.append("../services/status_led")
import mod_state_file  # pylint: disable=E0401
#pylint: enable=wrong-import-position

class UnitTestsModStateFile(unittest.TestCase):
    '''
    Tests for the mod_state_file.py
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
    # Tests for service.status_led.mod_state_file
    # =========================================================================
    def test_valid_state(self):
        '''
        Test mod_state_file.valid_state(state)
        '''
        self.assertFalse(mod_state_file.StateFile().valid_state(""))
        self.assertFalse(mod_state_file.StateFile().valid_state("10"))
        self.assertFalse(mod_state_file.StateFile().valid_state("1000"))
        self.assertFalse(mod_state_file.StateFile().valid_state("-10"))
        self.assertFalse(mod_state_file.StateFile().valid_state("abc"))
        self.assertTrue(mod_state_file.StateFile().valid_state("000"))
        self.assertTrue(mod_state_file.StateFile().valid_state("111"))
        self.assertTrue(mod_state_file.StateFile().valid_state("222"))
        self.assertTrue(mod_state_file.StateFile().valid_state("100"))
        self.assertTrue(mod_state_file.StateFile().valid_state("010"))
        self.assertTrue(mod_state_file.StateFile().valid_state("001"))
        self.assertTrue(mod_state_file.StateFile().valid_state("200"))
        self.assertTrue(mod_state_file.StateFile().valid_state("020"))
        self.assertTrue(mod_state_file.StateFile().valid_state("002"))
        self.assertTrue(mod_state_file.StateFile().valid_state("222"))
        self.assertFalse(mod_state_file.StateFile().valid_state("223"))
        self.assertFalse(mod_state_file.StateFile().valid_state("003"))
        self.assertTrue(mod_state_file.StateFile().valid_state("211"))
        self.assertTrue(mod_state_file.StateFile().valid_state("121"))
        self.assertTrue(mod_state_file.StateFile().valid_state("112"))

    def test_get_state_file(self):
        '''
        Test mod_state_file.get_state_file() - Get State File Path
        '''
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
        self.assertEqual(mod_state_file.StateFile().state_file(), goodpath)
        self.assertNotEqual(mod_state_file.StateFile().state_file(), badpath)

    def test_read_write_exceptions(self):
        '''
        Test Read with No File.
        '''
        with self.assertRaises(IOError):
            mod_state_file.StateFile().read()

        with self.assertRaises(ValueError):
            mod_state_file.StateFile().write("")
        with self.assertRaises(ValueError):
            mod_state_file.StateFile().write("10")
        with self.assertRaises(ValueError):
            mod_state_file.StateFile().write("1000")
        with self.assertRaises(ValueError):
            mod_state_file.StateFile().write("-10")
        with self.assertRaises(ValueError):
            mod_state_file.StateFile().write("300")
        with self.assertRaises(ValueError):
            mod_state_file.StateFile().write("abc")
        with self.assertRaises(ValueError):
            mod_state_file.StateFile().init("abc")

    def test_read_write_test(self):
        '''
        Test Read and Write
        '''
        self.assertEqual(mod_state_file.StateFile().init(), "000")
        self.assertEqual(mod_state_file.StateFile().read(), "000")
        self.assertNotEqual(mod_state_file.StateFile().read(), "001")
        self.assertEqual(mod_state_file.StateFile().init("010"), "010")
        self.assertNotEqual(mod_state_file.StateFile().write("100"), "000")
        self.assertEqual(mod_state_file.StateFile().read(), "100")

if __name__ == '__main__':
    unittest.main()
