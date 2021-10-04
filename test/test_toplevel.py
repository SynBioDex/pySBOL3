import os
import posixpath
import unittest

import sbol3

# See https://github.com/SynBioDex/pySBOL3/issues/264
# Data for "test_no_namespace_in_file" test case  below.
# The object in this data lacks a namespace, and that
# should be the case after the file is loaded.
TEST_DATA = """@prefix sbol: <http://sbols.org/v3#> .

<http://sbols.org/unspecified_namespace/foo> a sbol:Component ;
    sbol:displayId "foo" ;
    sbol:type <https://identifiers.org/SBO:0000251> .
"""

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestTopLevel(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_default_namespace(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/263
        display_id = 'foo'
        with self.assertWarns(UserWarning) as cm:
            c = sbol3.Component(display_id, sbol3.SBO_DNA)
        # Verify that the generated warning says something about sbol3.set_namespace
        self.assertIn('set_namespace', str(cm.warning))
        # Ensure that the component has a namespace. This was bug 263, see link above
        self.assertIsNotNone(c.namespace)
        self.assertTrue(c.identity.endswith(display_id))
        self.assertEqual(c.identity, posixpath.join(c.namespace, display_id))

    def test_no_namespace_in_file(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/264
        doc = sbol3.Document()
        doc.read_string(TEST_DATA, 'ttl')
        self.assertEqual(1, len(doc.objects))
        obj = doc.objects[0]
        self.assertIsInstance(obj, sbol3.Component)
        self.assertIsNone(obj.namespace)
        # We expect validation warnings on this test document
        # because the object lacks a namespace
        report = doc.validate()
        self.assertTrue(len(report) > 0)

    def test_copy(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/176 reopened
        # Copying a tree of objects to a new document left the document
        # pointer of the child objects unset. This caused "lookup" to
        # fail.
        dest_doc = sbol3.Document()

        def check_document(i: sbol3.Identified):
            # Verify that the object has a document, and that it is the
            # expected document.
            self.assertIsNotNone(i.document)
            self.assertEqual(dest_doc, i.document)

        test_path = os.path.join(SBOL3_LOCATION, 'multicellular',
                                 'multicellular.nt')
        doc = sbol3.Document()
        doc.read(test_path)
        for obj in doc.objects:
            obj.copy(target_doc=dest_doc)
        self.assertEqual(len(doc), len(dest_doc))
        for obj in dest_doc.objects:
            obj.traverse(check_document)


if __name__ == '__main__':
    unittest.main()
