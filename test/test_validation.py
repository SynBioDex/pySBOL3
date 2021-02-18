import unittest

import sbol3


class TestValidationReport(unittest.TestCase):

    def test_boolean(self):
        # False if no errors or warnings
        report = sbol3.ValidationReport()
        self.assertEqual(False, bool(report))
        # True if any errors
        report.addError(None, None, 'Fake error')
        self.assertEqual(True, bool(report))
        # True if any warnings
        report = sbol3.ValidationReport()
        report.addWarning(None, None, 'Fake warning')
        self.assertEqual(True, bool(report))
        # True if both errors and warnings
        report = sbol3.ValidationReport()
        report.addError(None, None, 'Fake error')
        report.addWarning(None, None, 'Fake warning')
        self.assertEqual(True, bool(report))

    def test_length(self):
        # Length should be the sum of errors and warnings
        report = sbol3.ValidationReport()
        self.assertEqual(0, len(report))
        report.addError(None, None, 'Fake error')
        self.assertEqual(1, len(report))
        report.addWarning(None, None, 'Fake warning')
        self.assertEqual(2, len(report))


if __name__ == '__main__':
    unittest.main()
