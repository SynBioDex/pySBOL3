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

    def test_shacl_closure_with_toplevels(self):
        # SBOL closure semantics should allow properties to reference
        # a TopLevel object not contained in the Document
        doc = sbol3.Document()
        doc.read(os.path.join(TEST_DIR, 'resources', 'package.nt'))
        self.assertEqual(len(doc.validate()), 0) 
        minidoc = sbol3.Document()
        c = doc.find('https://synbiohub.org/public/igem/BBa_I20270')
        c.copy(minidoc)
        self.assertEqual(len(minidoc.validate()), 0)  # this assertion fails

    @unittest.expectedFailure
    def test_shacl_closure_with_child_objects(self):
        # See issue #348
        sbol3.set_namespace('http://foo.org/')
        doc = sbol3.Document()
        c_top = sbol3.Component('top', sbol3.SBO_DNA)
        c_middle = sbol3.Component('middle', sbol3.SBO_DNA)
        c_bottom = sbol3.Component('bottom', sbol3.SBO_DNA)
        subc_middle = sbol3.SubComponent(c_middle)
        c_top.features = [subc_middle]
        subc_bottom = sbol3.SubComponent(c_bottom)
        c_middle.features = [subc_bottom]
        subc_bottom_ref = sbol3.ComponentReference(in_child_of=subc_middle, refers_to=subc_bottom)
        c_top.features.append(subc_bottom_ref)
        doc.add(c_top)
        self.assertFalse(len(doc.validate()))


if __name__ == '__main__':
    unittest.main()

