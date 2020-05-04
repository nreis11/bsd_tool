import os
import unittest
import filecmp
from context import data
from data import tpl_parser

TEST_DIR = "tests/"


class TestTpl_Parser(unittest.TestCase):

    def tearDown(self):
        test_output = TEST_DIR + "sampler_result.js"
        if os.path.exists(test_output):
            print("Removing", test_output)
            os.remove(test_output)

    def test_output(self):
        """Test that script returns correct output"""
        tpl_parser.main(test=True)
        self.assertTrue(filecmp.cmp(
            TEST_DIR + "sampler_bsd3.js", TEST_DIR + "sampler_result.js"))


if __name__ == '__main__':
    unittest.main()
