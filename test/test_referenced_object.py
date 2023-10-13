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

    TEST_SBOL = '''
@base          <https://sbolstandard.org/examples/> .
@prefix :      <https://sbolstandard.org/examples/> .
@prefix sbol:  <http://sbols.org/v3#> .
@prefix SBO:   <https://identifiers.org/SBO:> .

:toggle_switch  a          sbol:Component ;
        sbol:description   "Toggle Switch genetic circuit" ;
        sbol:displayId     "toggle_switch" ;
        sbol:hasModel      :model1 ;
        sbol:hasNamespace  <https://sbolstandard.org/examples> ;
        sbol:name          "Toggle Switch" ;
        sbol:type          SBO:0000241 .'''

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
        self.assertFalse(type(model) is rdflib.URIRef)
        self.assertTrue(type(model) is sbol3.Model)
        self.assertTrue(hasattr(model, 'lookup'), f'{model}')
        self.assertEqual('https://sbolstandard.org/examples/model1', model.identity)

        # Test reverse compatibility with lookup
        model_lookup = model.lookup()
        self.assertTrue(model_lookup is model)

    def test_parse_external_reference(self):
        # When parsing a document, if we encounter a reference to an object 
        # not in this document, create a stub object using SBOLObject
        test_format = sbol3.TURTLE

        doc = sbol3.Document()
        doc.read_string(TestReferencedObject.TEST_SBOL, file_format=test_format)
        component = doc.find('toggle_switch')
        model = component.models[0]
        self.assertTrue(type(model) is sbol3.SBOLObject)
        self.assertEqual(model.identity, 'https://sbolstandard.org/examples/model1')

    def test_serialize_external_reference(self):
        # When serializing a document, if we encounter a reference to an object 
        # not in this document, serialize it as a URI
        test_format = sbol3.TURTLE

        doc = sbol3.Document()
        doc2 = sbol3.Document()

        doc.read_string(TestReferencedObject.TEST_SBOL, file_format=test_format)
        component = doc.find('toggle_switch')
        model = component.models[0]
        self.assertTrue(type(model) is sbol3.SBOLObject)
        self.assertEqual(model.identity, 'https://sbolstandard.org/examples/model1')

        doc2.read_string(doc.write_string(file_format=test_format), file_format=test_format)
        component = doc2.find('toggle_switch')
        model = component.models[0]


    def test_copy(self):
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model', 'model.ttl')
        test_format = sbol3.TURTLE

        doc = sbol3.Document()
        doc2 = sbol3.Document()

        doc.read(test_path, test_format)
        component = doc.find('toggle_switch')
        model = component.models[0]
        self.assertTrue(type(model) is sbol3.Model)

        # When the Component is copied to a new document,
        # its reference to the Sequence should be treated as an external reference
        component_copy = component.copy(target_doc=doc2)
        model = component_copy.models[0]
        self.assertTrue(type(model) is sbol3.SBOLObject)


    def test_insert_into_list(self):
        # Test assignment using list indices
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)
        seq1 = sbol3.Sequence('seq1')
        seq2 = sbol3.Sequence('seq2')
        doc.add(component)
        doc.add(seq1)
        doc.add(seq2)
        component.sequences = [seq1]
        self.assertIn(component, seq1._references)

        component.sequences[0] = seq1
        self.assertIn(component, seq1._references)
        self.assertEqual(len(seq1._references), 1)

        component.sequences[0] = seq2
        self.assertIn(component, seq2._references)
        self.assertNotIn(component, seq1._references)

    def test_uri_assignment_and_resolution(self):
        # Test assignment to a ReferencedObject attribute with a URI string
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)
        seq1 = sbol3.Sequence('seq1')
        seq2 = sbol3.Sequence('seq2')
        doc.add(component)
        doc.add(seq1)
        doc.add(seq2)

        component.sequences.append(seq1.identity)
        self.assertEqual(list(component.sequences), [seq1])
        self.assertListEqual(seq1._references, [component])

        component.sequences = [seq1.identity]
        self.assertListEqual(list(component.sequences), [seq1])
        self.assertListEqual(seq1._references, [component])

        component.sequences = [seq1.identity, seq2.identity]
        self.assertListEqual(list(component.sequences), [seq1, seq2])

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
        # Test assignment to a ReferencedObject attribute with a URI string
        doc = sbol3.Document()
        sbol3.set_namespace('https://example.org')
        foo = sbol3.Collection('https://example.org/baz')
        doc.add(foo)

        execution = sbol3.Activity('protocol_execution')
        self.assertFalse(execution in foo._owned_objects[sbol3.SBOL_MEMBER])
        foo.members.append(execution)
        self.assertTrue(execution in foo._referenced_objects[sbol3.SBOL_MEMBER])
        self.assertFalse(execution in foo._owned_objects[sbol3.SBOL_MEMBER])

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

    def test_equality(self):
        # Test comparison of a referenced object to a URI, in order
        # to maintain reverse compatibility
        foo = sbol3.SBOLObject('foo')
        self.assertEqual(foo, foo.identity)
        self.assertEqual(foo.identity, foo)
 
    def test_singleton_property_reference_counter(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        root = sbol3.Component('root', sbol3.SBO_DNA)
        sub = sbol3.Component('sub', sbol3.SBO_DNA)

        doc.add(root)
        doc.add(sub)

        feature = sbol3.SubComponent(instance_of=root)
        root.features.append(feature)
        self.assertEqual(root._references, [feature])

    def test_list_property_reference_counter(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)

        # Test that the reference counter is initialized
        seq1 = sbol3.Sequence('seq1')
        self.assertListEqual(seq1._references, [])
        doc.add(component)
        doc.add(seq1)
        
        # Test that the reference counter is working
        component.sequences = [seq1.identity]
        self.assertListEqual(seq1._references, [component])

        # Test that the reference counter is cleared
        component.sequences = []
        self.assertListEqual(seq1._references, [])

        # Test that the reference counter works with the append method
        component.sequences.append(seq1.identity)
        self.assertListEqual(seq1._references, [component])

        # Test that the reference counter is cleared
        component.sequences.remove(seq1)
        self.assertListEqual(seq1._references, [])

    def test_update(self):
        # Update and resolve references to an external object when the object is
        # added to the Document
        pass

if __name__ == '__main__':
    unittest.main()
