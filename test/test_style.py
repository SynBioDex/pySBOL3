import os
import sys
import unittest

try:
    import pycodestyle
except ModuleNotFoundError:
    # The pycodestyle test will be skipped if the module is not available
    pass


MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
# The sbol2 directory is a sibling to the test directory where this file
# lives.
SBOL_PATH = os.path.join(os.path.dirname(MODULE_LOCATION), 'sbol3')
TEST_PATH = MODULE_LOCATION
EXAMPLES_PATH = os.path.join(os.path.dirname(MODULE_LOCATION), 'examples')
SETUP_PATH = os.path.join(os.path.dirname(MODULE_LOCATION), 'setup.py')
STYLE_CONFIG = os.path.join(os.path.dirname(MODULE_LOCATION), 'setup.cfg')

# Please don't increase this number!
MAX_WILDCARD_IMPORTS = 0

# -----------------------------------------------------------------
# Locale Fix
#
# If you get an ascii conversion error, you probably do not have a
# local set.
#
# Follow these steps, substituting for "en_US.utf8" as appropriate:
#
#     apt update
#     apt install locales
#     locale-gen en_US.utf8
#     export LANG=en_US.utf8
#
# -----------------------------------------------------------------


class TestStyle(unittest.TestCase):

    @unittest.skipUnless('pycodestyle' in sys.modules, "pycodestyle not available")
    def test_pep8(self):
        # Test that we conform to PEP-8 via `pycodestyle`
        # Set quiet to `False` to see the style issues
        quiet = True
        style = pycodestyle.StyleGuide(quiet=quiet,
                                       config_file=STYLE_CONFIG)
        style.options.report.start()
        style.input_dir(SBOL_PATH)
        style.input_dir(TEST_PATH)
        style.input_dir(EXAMPLES_PATH)
        style.input_file(SETUP_PATH)
        style.options.report.stop()
        result = style.options.report
        # Please try not to increase the expected number of errors. Please.
        expected_errors = 0
        msg = f'Found {result.total_errors} code style errors (and warnings).'
        self.assertLessEqual(result.total_errors, expected_errors, msg)


if __name__ == '__main__':
    unittest.main()
