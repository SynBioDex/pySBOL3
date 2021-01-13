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
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)
        sequence = sbol3.Sequence('seq1')
        doc.add(component)
        component.sequences.append(sequence)
        seq2_uri = component.sequences[0]
        self.assertEqual(sequence.identity, seq2_uri)
        seq = seq2_uri.lookup()
        self.assertIsNotNone(seq)
        self.assertEqual(sequence, seq)

    def test_instance_assignment(self):
        # Test assignment to a ReferencedObject attribute with an
        # instance using assignment
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)
        sequence = sbol3.Sequence('seq1')
        doc.add(component)
        component.sequences = [sequence]
        seq2_uri = component.sequences[0]
        self.assertEqual(sequence.identity, seq2_uri)
        seq = seq2_uri.lookup()
        self.assertIsNotNone(seq)
        self.assertEqual(sequence, seq)

    def test_singleton_assignment(self):
        # Test assignment to a ReferencedObject attribute with an
        # instance using assignment
        doc = sbol3.Document()
        test_parent = SingleRefObj('sro1')
        sequence = sbol3.Sequence('seq1')
        doc.add(test_parent)
        test_parent.sequence = sequence
        seq2_uri = test_parent.sequence
        self.assertEqual(sequence.identity, seq2_uri)
        seq = seq2_uri.lookup()
        self.assertIsNotNone(seq)
        self.assertEqual(sequence, seq)


if __name__ == '__main__':
    unittest.main()
