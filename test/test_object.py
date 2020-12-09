import posixpath
import unittest

import sbol3


class TestObject(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def test_trailing_slash(self):
        # A trailing slash on an object's identity should automatically be removed
        sbol3.set_namespace('http://example.org/sbol3')
        slash_identity = posixpath.join(sbol3.get_namespace(), 'c1', '')
        self.assertTrue(slash_identity.endswith(posixpath.sep))
        c = sbol3.Component(slash_identity, sbol3.SBO_DNA)
        identity = slash_identity.strip(posixpath.sep)
        self.assertEqual(identity, c.identity)

    def test_copy_properties(self):
        doc = sbol3.Document()
        root = sbol3.Component('root', sbol3.SBO_DNA)
        root.name = 'foo'
        root_copy = root.copy()
        self.assertEqual(root_copy.name, 'foo')

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
