import unittest

import sbol3


class TestModule(unittest.TestCase):

    def test_data_model(self):
        self.assertIsInstance(sbol3.Identified, type)
        self.assertIsInstance(sbol3.TopLevel, type)
        self.assertIsInstance(sbol3.Sequence, type)
        self.assertIsInstance(sbol3.Component, type)
        self.assertIsInstance(sbol3.SubComponent, type)
        self.assertIsInstance(sbol3.ComponentReference, type)
        self.assertIsInstance(sbol3.LocalSubComponent, type)
        self.assertIsInstance(sbol3.ExternallyDefined, type)
        self.assertIsInstance(sbol3.SequenceFeature, type)
        self.assertIsInstance(sbol3.Range, type)
        self.assertIsInstance(sbol3.Cut, type)
        self.assertIsInstance(sbol3.EntireSequence, type)
        self.assertIsInstance(sbol3.Constraint, type)
        self.assertIsInstance(sbol3.Interaction, type)
        self.assertIsInstance(sbol3.Participation, type)
        self.assertIsInstance(sbol3.Interface, type)
        self.assertIsInstance(sbol3.CombinatorialDerivation, type)
        self.assertIsInstance(sbol3.VariableComponent, type)
        self.assertIsInstance(sbol3.Implementation, type)
        self.assertIsInstance(sbol3.ExperimentalData, type)
        self.assertIsInstance(sbol3.Model, type)
        self.assertIsInstance(sbol3.Collection, type)
        self.assertIsInstance(sbol3.Namespace, type)
        self.assertIsInstance(sbol3.Experiment, type)
        self.assertIsInstance(sbol3.Attachment, type)


if __name__ == '__main__':
    unittest.main()
