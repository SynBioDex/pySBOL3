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

    def test_str(self):
        # str representation should consist of errors and warnings
        # all errors precede any warning
        report = sbol3.ValidationReport()
        self.assertEqual('', str(report))
        report.addError(None, None, 'Fake error')
        self.assertEqual('Fake error', str(report))
        report.addWarning(None, None, 'Fake warning')
        self.assertEqual('Fake error\nFake warning', str(report))
        report.addError(None, None, 'Fake error')
        self.assertEqual('Fake error\nFake error\nFake warning', str(report))

    def test_shacl_closure_with_toplevels(self):
        # SBOL closure semantics should allow properties to reference
        # a TopLevel object not contained in the Document
        # This is the test case in https://github.com/SynBioDex/pySBOL3/issues/348
        doc = sbol3.Document()
        doc.read(os.path.join(TEST_DIR, 'resources', 'package.nt'))
        self.assertEqual(len(doc.validate()), 0)
        minidoc = sbol3.Document()
        c = doc.find('https://synbiohub.org/public/igem/BBa_I20270')
        self.assertIsInstance(c, sbol3.TopLevel)
        sbol3.copy([c], into_document=minidoc)
        # this assertion failed before the fix to the shacl rules
        self.assertEqual(len(minidoc.validate()), 0)

    def test_shacl_closure_simple(self):
        # This is a very small test case to reproduce the issue at the
        # center of https://github.com/SynBioDex/pySBOL3/issues/348
        sbol3.set_namespace('https://github.com/SynBioDex/pySBOL3')
        other_component = 'https://github.com/SynBioDex/pySBOL3/other_c'
        sc = sbol3.SubComponent(instance_of=other_component)
        c = sbol3.Component('c1', types=[sbol3.SBO_DNA], features=[sc])
        doc = sbol3.Document()
        doc.add(c)
        report = doc.validate()
        self.assertEqual(0, len(report))

    @unittest.expectedFailure
    def test_shacl_closure_with_child_objects(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/348
        # See https://github.com/SynBioDex/pySBOL3/issues/353
        sbol3.set_namespace('https://github.com/SynBioDex/pySBOL3')
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
