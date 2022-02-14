import posixpath
import unittest
import uuid

import rdflib

import sbol3


class TestIdentified(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_display_name(self):
        """Tests display_name property which must return display_id
        if name doesn't exist, else return name of the identified object
        """
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        test_name = 'Test_name'
        test_display_id = 'Test_display_id'
        # case 1. only identity provided
        obj_without_name = sbol3.Component(test_display_id, sbol3.SBO_DNA)
        display_name = obj_without_name.display_name
        self.assertEqual(display_name, test_display_id)
        # case 2. both name and identity provided
        obj_with_name = sbol3.Component(
            test_display_id, sbol3.SBO_DNA, name=test_name)
        display_name = obj_with_name.display_name
        self.assertEqual(display_name, test_name)

    def test_display_id(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1_display_id = 'c1'
        c = sbol3.Component(c1_display_id, sbol3.SBO_DNA)
        self.assertEqual(c1_display_id, c.display_id)
        self.assertIsInstance(c.display_id, str)
        display_id = 'my_component'
        # Ensure that displayId cannot be set
        with self.assertRaises(AttributeError):
            c.display_id = display_id
        # Should still have the old value
        self.assertEqual(c1_display_id, c.display_id)
        # Under the covers
        self.assertIsInstance(c._properties[sbol3.SBOL_DISPLAY_ID][0],
                              rdflib.Literal)

    def test_identity_display_id(self):
        # Test setting of display_id
        #   * Test by passing display_id to constructor
        #   * Test by having display_id deduced from identity
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1_display_id = 'c1'
        c1_identity = posixpath.join(sbol3.get_namespace(), c1_display_id)
        c1 = sbol3.Component(c1_display_id, sbol3.SBO_DNA)
        self.assertEqual(c1_display_id, c1.display_id)
        self.assertEqual(c1_identity, c1.identity)
        # Now test identity and display_id from a URL-type URI
        c2_display_id = 'c2'
        c2_identity = posixpath.join(sbol3.get_namespace(), c2_display_id)
        c2 = sbol3.Component(c2_identity, sbol3.SBO_DNA)
        self.assertEqual(c2_display_id, c2.display_id)
        self.assertEqual(c2_identity, c2.identity)

    def test_uuid(self):
        # Verify that a UUID can be used as an identity and that
        # the object does not have a display_id since the identity
        # is not a URL
        identity = str(uuid.uuid5(uuid.NAMESPACE_URL,
                                  'https://github.com/synbiodex/pysbol3'))
        namespace = str(uuid.uuid4())
        c = sbol3.Component(identity, sbol3.SBO_DNA, namespace=namespace)
        self.assertEqual(identity, c.identity)
        self.assertIsNone(c.display_id)

    def test_basic_serialization(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c = sbol3.Component('c1', sbol3.SBO_DNA)
        graph = rdflib.Graph()
        c.serialize(graph)
        # Is there a better way to get all the triples?
        triples = list(graph.triples((None, None, None)))
        # Expecting a triple for the type, a triple for the displayId,
        # a triple for the namespace, and a triple for the component type
        self.assertEqual(4, len(triples))

    def test_singleton_wrapping_urls(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        process1 = 'https://example.com/thing'
        thing = sbol3.Sequence('thing1', derived_from=process1)
        self.assertEqual(1, len(thing.derived_from))
        self.assertEqual(process1, thing.derived_from[0])

    def test_extract_display_id(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/310
        # Ensure that extract_display_id is a public function
        self.assertIn('extract_display_id', dir(sbol3))
        # Ensure that is_valid_display_id is a public function
        self.assertIn('is_valid_display_id', dir(sbol3))


if __name__ == '__main__':
    unittest.main()
