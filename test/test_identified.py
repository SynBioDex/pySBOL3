import posixpath
import unittest
import uuid

import rdflib

import sbol3


class TestIdentified(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def test_display_id(self):
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
        identity = str(uuid.uuid5(uuid.NAMESPACE_URL, sbol3.get_namespace()))
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

    def test_copy_properties(self):
        doc = sbol3.Document()
        i = sbol3.Identified('i', type_uri='http://example.org#Identified')
        i.name = 'foo'
        print(dir(i))
        i_copy = i.copy()
        self.assertEqual(i_copy.name, 'foo')

    def test_copy_child_objects(self):
        doc = sbol3.Document()
        root = sbol3.Component('root', sbol3.SBO_DNA)
        sub1 = sbol3.Component('sub1', sbol3.SBO_DNA)
        sub2 = sbol3.Component('sub2', sbol3.SBO_DNA)
        sc1 = sbol3.SubComponent(sub1)
        sc2 = sbol3.SubComponent(sub2)
        root.features.append(sc1)
        root.features.append(sc2)
        doc.add(root)
        doc.add(sub1)
        doc.add(sub2)

        doc2 = sbol3.Document()
        root_copy = root.copy(target_doc=doc2)
        self.assertEqual([sc.identity for sc in root.features],
                         [sc.identity for sc in root_copy.features])

    # def test_import_object_into_new_namespace(self):
    #     # When copying an object into a new namespace, confirm that it's URI is copied
    #     # into the new namespace. Also confirm that any ReferencedObject attributes
    #     # whose values point to an object in the old namespace are also copied into the
    #     # new namespace
    #     sbol3.setHomespace('http://examples.org')
    #     sbol3.Config.setOption(sbol2.ConfigOptions.SBOL_COMPLIANT_URIS, True)
    #     sbol3.Config.setOption(sbol2.ConfigOptions.SBOL_TYPED_URIS, False)
    #     doc = sbol3.Document()
    #     comp = sbol3.ComponentDefinition('cd')
    #     seq = sbol3.Sequence('seq')
    #     doc.addComponentDefinition(comp)
    #     doc.addSequence(seq)
    #     comp.sequences = seq.identity

    #     # Import from old homespace into new homespace
    #     old_homespace = sbol3.getHomespace()
    #     sbol3.setHomespace('http://acme.com')
    #     comp_copy = comp.copy(None, old_homespace)

    #     # Verify new namespace was correctly substituted
    #     self.assertEqual(comp_copy.identity, 'http://acme.com/cd/1')
    #     self.assertEqual(comp_copy.persistentIdentity, 'http://acme.com/cd')
    #     self.assertEqual(comp_copy.sequences[0], 'http://acme.com/seq/1')

    #     # Verify wasDerivedFrom relationship
    #     self.assertEqual(comp_copy.wasDerivedFrom[0], comp.identity)

    #     # Ensure these are equal under the covers
    #     self.assertEqual(type(comp.properties[sbol3.SBOL_SEQUENCE_PROPERTY][0]),
    #                      rdflib.URIRef)
    #     self.assertEqual(type(comp.properties[sbol3.SBOL_SEQUENCE_PROPERTY][0]),
    #                      type(comp_copy.properties[sbol3.SBOL_SEQUENCE_PROPERTY][0]))


if __name__ == '__main__':
    unittest.main()
