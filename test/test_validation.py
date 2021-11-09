import unittest
import os

import sbol3


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


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

    def test_shacl_closure(self):
        doc = sbol3.Document()
        doc.read(os.path.join(TEST_DIR, 'resources', 'package.nt'))
        #for e in doc.validate():
        #     print(e)
        #self.assertEqual(len(doc.validate()), 0)
        
        minidoc = sbol3.Document()
        c = doc.find('https://synbiohub.org/public/igem/BBa_I20270')
        c.copy(minidoc)

        for e in minidoc.validate():
             print(e)
        self.assertEqual(len(minidoc.validate()), 0)  # this assertion fails


if __name__ == '__main__':
    unittest.main()
