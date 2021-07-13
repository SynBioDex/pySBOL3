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


class MyTestCase(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
