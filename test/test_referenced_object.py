import os
import unittest

import sbol3
import rdflib


MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class SingleRefObj(sbol3.TopLevel):

    SRO_URI = 'https://github.com/synbiodex/sbol3#SingleRefObj'
    SEQUENCE_URI = 'https://github.com/synbiodex/sbol3#sequence'

    def __init__(self, identity: str, type_uri: str = SRO_URI):
        super().__init__(identity, type_uri)
        self.sequence = sbol3.ReferencedObject(self, SingleRefObj.SEQUENCE_URI, 0, 1)


class TestReferencedObject(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_parse_refobj(self):
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model', 'model.ttl')
        test_format = sbol3.TURTLE

        doc = sbol3.Document()
        doc.read(test_path, test_format)
        component = doc.find('toggle_switch')
        self.assertIsNotNone(component)
        model = component.models[0]
        print('Model:', model)
        print(type(model))
        self.assertFalse(type(model) is rdflib.URIRef)
        self.assertTrue(type(model) is sbol3.Model)
        self.assertTrue(hasattr(model, 'lookup'), f'{model}')
        self.assertEqual('https://sbolstandard.org/examples/model1', model.identity)
        model = model.lookup()
        self.assertIsNotNone(model)

    def test_uri_assignment_and_resolution(self):
        # Test assignment to a ReferencedObject attribute with a URI string
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)
        sequence = sbol3.Sequence('seq1')
        doc.add(component)
        doc.add(sequence)
        component.sequences.append(sequence.identity)
        self.assertEqual(sequence, component.sequences[0])

    def test_uri_assignment_not_resolved(self):
        # Test assignment to a ReferencedObject attribute with a URI string
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)
        sequence = sbol3.Sequence('seq1')
        doc.add(component)

        # Because the Sequence is not contained in the Document,
        # we can't resolve the reference
        component.sequences.append(sequence.identity)
        self.assertNotEqual(sequence, component.sequences[0])
        self.assertTrue(type(component.sequences[0]) is sbol3.SBOLObject)
 

    def test_instance_append(self):
        # Test assignment to a ReferencedObject attribute with an
        # instance using append
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)
        sequence = sbol3.Sequence('seq1')
        doc.add(component)
        doc.add(sequence)
        component.sequences.append(sequence)
        self.assertEqual(sequence, component.sequences[0])

    def test_instance_assignment(self):
        # Test assignment to a ReferencedObject attribute with an
        # instance using assignment
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)
        sequence = sbol3.Sequence('seq1')
        doc.add(component)
        doc.add(sequence)
        component.sequences = [sequence]
        self.assertEqual(component.sequences[0], sequence)

    def test_lookup_reverse_compatible(self):
        pass

    def test_singleton_assignment(self):
        # Test assignment to a ReferencedObject attribute with an
        # instance using assignment
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        test_parent = SingleRefObj('sro1')
        sequence = sbol3.Sequence('seq1')
        doc.add(test_parent)
        doc.add(sequence)
        test_parent.sequence = sequence
        self.assertEqual(test_parent.sequence, sequence)

    def test_adding_referenced_objects(self):
        # Verify that sbol3 does not try to add objects
        # to the document when they are added to a referenced
        # object property.
        #
        # See https://github.com/SynBioDex/pySBOL3/issues/184
        doc = sbol3.Document()
        sbol3.set_namespace('https://example.org')
        execution = sbol3.Activity('protocol_execution')
        doc.add(execution)
        foo = sbol3.Collection('https://example.org/baz')
        foo.members.append(execution)
        # Verify that foo did not get document assigned
        self.assertIsNone(foo.document)
        # Now explicitly add foo to the document and ensure
        # everything works as expected
        doc.add(foo)
        self.assertEqual(execution, foo.members[0])

    def test_adding_referenced_objects(self):
        # Verify that sbol3 does not try to add objects
        # to the document when they are added to a referenced
        # object property.
        #
        # See https://github.com/SynBioDex/pySBOL3/issues/184
        # Test assignment to a ReferencedObject attribute with a URI string
        doc = sbol3.Document()
        sbol3.set_namespace('https://example.org')
        foo = sbol3.Collection('https://example.org/baz')
        doc.add(foo)

        execution = sbol3.Activity('protocol_execution')
        foo.members.append(execution)
        # Verify that execution did not get document assigned
        self.assertIsNone(execution.document)
        self.assertNotIn(execution, doc.objects)

        # Now explicitly add foo to the document and ensure
        # everything works as expected
        doc.add(execution)
        foo.members.append(execution)
        self.assertEqual(execution, foo.members[0])
        

    def test_no_identity_exception(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/357
        sbol3.set_namespace('https://github.com/SynBioDex/pySBOL3')
        collection = sbol3.Collection('foo_collection')
        subc = sbol3.SubComponent(instance_of='https://github.com/SynBioDex/pySBOL3/c1')
        exc_regex = r'Object identity is uninitialized\.$'
        with self.assertRaisesRegex(ValueError, exc_regex):
            collection.members.append(subc)


if __name__ == '__main__':
    unittest.main()
