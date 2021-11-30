import os
import unittest

import sbol3

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

    def test_lookup(self):
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model', 'model.ttl')
        test_format = sbol3.TURTLE

        doc = sbol3.Document()
        doc.read(test_path, test_format)
        component = doc.find('toggle_switch')
        self.assertIsNotNone(component)
        model_uri = component.models[0]
        self.assertTrue(isinstance(model_uri, str))
        self.assertTrue(hasattr(model_uri, 'lookup'))
        self.assertEqual('https://sbolstandard.org/examples/model1', model_uri)
        model = model_uri.lookup()
        self.assertIsNotNone(model)

    def test_uri_assignment(self):
        # Test assignment to a ReferencedObject attribute with a URI string
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)
        sequence = sbol3.Sequence('seq1')
        doc.add(component)
        doc.add(sequence)
        component.sequences.append(sequence.identity)
        seq2_uri = component.sequences[0]
        self.assertEqual(sequence.identity, seq2_uri)
        seq = seq2_uri.lookup()
        self.assertIsNotNone(seq)
        self.assertEqual(sequence, seq)

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
        seq2_uri = component.sequences[0]
        self.assertEqual(sequence.identity, seq2_uri)
        seq = seq2_uri.lookup()
        self.assertIsNotNone(seq)
        self.assertEqual(sequence, seq)

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
        seq2_uri = component.sequences[0]
        self.assertEqual(sequence.identity, seq2_uri)
        seq = seq2_uri.lookup()
        self.assertIsNotNone(seq)
        self.assertEqual(sequence, seq)

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
        seq2_uri = test_parent.sequence
        self.assertEqual(sequence.identity, seq2_uri)
        seq = seq2_uri.lookup()
        self.assertIsNotNone(seq)
        self.assertEqual(sequence, seq)

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
        self.assertEqual(execution.identity, foo.members[0])
        # Also verify that we can use lookup on the object
        # to get back to the original instance via document lookup
        self.assertEqual(execution.identity, foo.members[0].lookup().identity)

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
