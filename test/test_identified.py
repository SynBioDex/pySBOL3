import posixpath
import unittest
import uuid

import rdflib

import sbol3


class TestIdentified(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def test_display_id(self):
        # self.assertEqual(None, sbol3.get_homespace())
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
        c1_display_id = 'c1'
        c1_identity = posixpath.join(sbol3.get_homespace(), c1_display_id)
        c1 = sbol3.Component(c1_display_id, sbol3.SBO_DNA)
        self.assertEqual(c1_display_id, c1.display_id)
        self.assertEqual(c1_identity, c1.identity)
        # Now test identity and display_id from a URL-type URI
        c2_display_id = 'c2'
        c2_identity = posixpath.join(sbol3.get_homespace(), c2_display_id)
        c2 = sbol3.Component(c2_identity, sbol3.SBO_DNA)
        self.assertEqual(c2_display_id, c2.display_id)
        self.assertEqual(c2_identity, c2.identity)

    def test_uuid(self):
        # Verify that a UUID can be used as an identity and that
        # the object does not have a display_id since the identity
        # is not a URL
        identity = str(uuid.uuid5(uuid.NAMESPACE_URL, sbol3.get_homespace()))
        c = sbol3.Component(identity, sbol3.SBO_DNA)
        self.assertEqual(identity, c.identity)
        self.assertIsNone(c.display_id)

    def test_basic_serialization(self):
        c = sbol3.Component('c1', sbol3.SBO_DNA)
        graph = rdflib.Graph()
        c.serialize(graph)
        # Is there a better way to get all the triples?
        triples = list(graph.triples((None, None, None)))
        # Expecting a triple for the type, a triple for the displayId,
        # and a triple for the component type
        self.assertEqual(3, len(triples))


if __name__ == '__main__':
    unittest.main()
