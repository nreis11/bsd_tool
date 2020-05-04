import unittest

# import your test modules
import test_input_control
import test_dropdown_control
import test_tpl_parser

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_tpl_parser))
suite.addTests(loader.loadTestsFromModule(test_input_control))
suite.addTests(loader.loadTestsFromModule(test_dropdown_control))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
