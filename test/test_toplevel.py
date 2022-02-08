import os
import posixpath
import unittest
import uuid

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
        sbol3.copy(doc, into_document=dest_doc)
        self.assertEqual(len(doc), len(dest_doc))
        for obj in dest_doc.objects:
            obj.traverse(check_document)

    def test_namespace_mismatch(self):
        # See SBOL 3 rule sbol3-10301
        # See https://github.com/SynBioDex/pySBOL3/issues/278
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c = sbol3.Component('foo', types=[sbol3.SBO_DNA])
        c.namespace = 'https://example.com/mismatch'
        report = c.validate()
        self.assertIsNotNone(report)
        # Expecting at least one error
        self.assertGreater(len(report), 0)

        # If the namespace is a URN, it doesn't matter if it is a mismatch
        c.namespace = uuid.uuid4().urn
        report = c.validate()
        self.assertIsNotNone(report)
        self.assertGreater(len(report), 0)

        # Now check a URN identity
        c = sbol3.Component(uuid.uuid4().urn, types=[sbol3.SBO_DNA])
        report = c.validate()
        self.assertIsNotNone(report)
        # Expecting at least one error
        self.assertEqual(len(report), 0)

    def test_namespace_mismatch_uuid(self):
        # Now check a UUID with no default namespace set
        # sbol3.set_namespace(None)
        self.assertIsNone(sbol3.get_namespace())
        c = sbol3.Component(uuid.uuid4().urn, types=[sbol3.SBO_DNA])
        report = c.validate()
        self.assertIsNotNone(report)
        # Expecting at least one error
        self.assertEqual(0, len(report))

    def test_default_namespace_with_local_path(self):
        # Make sure default namespace is honored when the identity has
        # a local path included
        test_namespace = 'https://github.com/synbiodex'
        sbol3.set_namespace(test_namespace)
        self.assertEqual(test_namespace, sbol3.get_namespace())
        identity = posixpath.join(sbol3.get_namespace(), 'pysbol3', 'foo')
        c = sbol3.Component(identity, types=[sbol3.SBO_DNA])
        self.assertEqual(sbol3.get_namespace(), c.namespace)
        self.assertEqual('foo', c.display_id)
        self.assertEqual(identity, c.identity)
        self.assertEqual(0, len(c.validate()))

    def test_creation_namespace_mismatch(self):
        # Prevent an identity/namespace mismatch on object creation
        # See https://github.com/SynBioDex/pySBOL3/issues/277
        with self.assertRaises(ValueError):
            sbol3.Component('https://example.com/mismatch/c1',
                            types=[sbol3.SBO_DNA],
                            namespace='https://example.com/different')

    def test_split_identity(self):
        namespace = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(namespace)
        name = 'c1'
        c1 = sbol3.Component(name, types=[sbol3.SBO_DNA])
        expected = namespace, '', name
        self.assertEqual(expected, c1.split_identity())
        # Test with an intermediate path
        name = 'c2'
        path = 'foo'
        c2_identity = posixpath.join(namespace, path, name)
        c2 = sbol3.Component(c2_identity, types=[sbol3.SBO_DNA])
        expected = namespace, path, name
        self.assertEqual(expected, c2.split_identity())
        # Test with a longer intermediate path
        name = 'c3'
        path = 'foo/bar/baz'
        c3_identity = posixpath.join(namespace, path, name)
        c3 = sbol3.Component(c3_identity, types=[sbol3.SBO_DNA])
        expected = namespace, path, name
        self.assertEqual(expected, c3.split_identity())

    def test_clone_bad_rename(self):
        # Tests that the dependent objects have consistent renaming
        namespace = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(namespace)
        name = 'c1'
        c1 = sbol3.Component(name, types=[sbol3.SBO_DNA])
        lsc1 = sbol3.LocalSubComponent(types=[sbol3.SBO_DNA])
        lsc2 = sbol3.LocalSubComponent(types=[sbol3.SBO_DNA])
        c1.features = [lsc1, lsc2]
        self.assertEqual('LocalSubComponent1', lsc1.display_id)
        self.assertEqual('LocalSubComponent2', lsc2.display_id)
        c1.features.remove(lsc1)
        self.assertListEqual([lsc2], list(c1.features))
        self.assertEqual('LocalSubComponent2', lsc2.display_id)
        self.assertIsNotNone(c1.find('LocalSubComponent2'))
        clone_name = 'c1_prime'
        c1_prime = c1.clone(posixpath.join(namespace, clone_name))
        self.assertIsNotNone(c1_prime.find('LocalSubComponent2'))

    def test_copy_is_deprecated(self):
        namespace = 'https://github.com/synbiodex/pysbol3'
        sbol3.set_namespace(namespace)
        name = 'c1'
        c1 = sbol3.Component(name, types=[sbol3.SBO_DNA])
        with self.assertWarns(DeprecationWarning):
            c1.copy()


if __name__ == '__main__':
    unittest.main()
