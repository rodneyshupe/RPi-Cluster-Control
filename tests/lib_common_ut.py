#!/usr/bin/env python
# pylint: disable=line-too-long
""" Unit Tests for the lib_common module """

import unittest # Documentation: https://docs.python.org/3.3/library/unittest.html

#pylint: disable=wrong-import-position
import sys
sys.path.append("..")
sys.path.append("../lib")
from lib_common import str_join, isnumeric
#pylint: enable=wrong-import-position

class TestForLibCommon(unittest.TestCase):
    """ Class contains unit tests. """
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

    def test_lib_common_str_join(self):
        """ Test str_join function """
        self.assertEqual(str_join("This", " is a ", "Test"), 'This is a Test')
        self.assertEqual(str_join("This", " is a ", "Test", 2), 'This is a Test2')
        self.assertEqual(str_join(12.34, " anouther test"), '12.34 anouther test')
        self.assertEqual(str_join("Anouther test"), 'Anouther test')
        self.assertEqual(str_join(12.34), '12.34')
        self.assertNotEqual(str_join("This", " is a ", "Test"), 'ThisTest')
        self.assertEqual(
            str_join({'This':1, 'is not':'a'}, 'Bad Test'),
            "{'This': 1, 'is not': 'a'}Bad Test"
        )
        #with self.assertRaises(TypeError):
        #    print(str_join([1,2,3],"Bad Test"))

    def test_lib_common_isnumeric(self):
        """ Test isnumeric function """
        self.assertTrue(isnumeric("0"))
        self.assertTrue(isnumeric("1"))
        self.assertTrue(isnumeric("-1"))
        self.assertTrue(isnumeric("1.23"))
        self.assertTrue(isnumeric(1.23))
        self.assertTrue(isnumeric("10"))
        self.assertTrue(isnumeric("100"))
        self.assertTrue(isnumeric("1000"))
        self.assertFalse(isnumeric("1,000"))
        self.assertTrue(isnumeric("-10"))
        self.assertTrue(isnumeric("-100"))
        self.assertTrue(isnumeric("-1000"))
        self.assertTrue(isnumeric("1.000"))
        self.assertTrue(isnumeric("-1.000"))
        self.assertFalse(isnumeric(""))
        self.assertFalse(isnumeric("Two"))
        self.assertFalse(isnumeric("1O")) # Note this is the letter O not a zero
        self.assertFalse(isnumeric([1, 2, 3]))
        self.assertFalse(isnumeric({"1":"2"}))

if __name__ == '__main__':
    unittest.main()
