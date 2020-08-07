import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestReferencedObject(unittest.TestCase):

    def test_lookup(self):
        test_path = os.path.join(SBOL3_LOCATION, 'entity', 'model', 'model.turtle.sbol')
        test_format = 'turtle'

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

    @unittest.expectedFailure
    def test_uri_assignment(self):
        # Test assignment to a ReferencedObject attribute with a URI string
        doc = sbol3.Document()
        component = sbol3.Component()
        sequence = sbol3.Sequence()
        doc.add(component)
        doc.add(sequence)
        component.sequences.append(sequence.identity)
        seq_uri = component.sequences[0]
        self.assertEqual(sequence.identity, seq_uri)
        seq = seq_uri.lookup()
        self.assertIsNotNone(seq)
        self.assertEqual(sequence, seq)

    @unittest.expectedFailure
    def test_instance_assignment(self):
        self.fail('Not implemented yet')
