import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from checker import *


class TestChecker(unittest.TestCase):

    def test_arg_parser(self):
        valid_args = {"test.json"}
        invalid_args = {"invalid!"}
        self.assertEqual(arg_parser(valid_args), "test.json")
        self.assertRaises(SystemExit, arg_parser, invalid_args)

    def test_check_rotated_file_size_param(self):
        valid_str_file_size = "10GB"
        invalid_str_file_size = "10DD"
        valid_int_file_size = 10000
        invalid_numeric_file_size = 10.25
        self.assertEqual(check_rotated_file_size_param(valid_str_file_size), 10737418240)
        self.assertRaises(SystemExit, check_rotated_file_size_param, invalid_str_file_size)
        self.assertEqual(check_rotated_file_size_param(valid_int_file_size), 10000)
        self.assertRaises(SystemExit, check_rotated_file_size_param, invalid_numeric_file_size)


if __name__ == '__main__':
    unittest.main()
