import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestComponentReference(unittest.TestCase):

    def test_create(self):
        identity = 'https://github.com/synbiodex/pysbol3/participation1'
        in_child_of = 'https://github.com/synbiodex/pysbol3/subcomponent'
        feature = 'https://github.com/synbiodex/pysbol3/other_feature'
        comp_ref = sbol3.ComponentReference(identity, in_child_of, feature)
        self.assertIsNotNone(comp_ref)
        self.assertEqual(in_child_of, comp_ref.in_child_of)
        self.assertEqual(feature, comp_ref.feature)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'toggle_switch',
                                 'toggle_switch.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        uri = 'https://sbolstandard.org/examples/toggle_switch/componentreference_1'
        comp_ref = doc.find(uri)
        self.assertIsNotNone(comp_ref)
        self.assertIsInstance(comp_ref, sbol3.ComponentReference)
        in_child_of = 'https://sbolstandard.org/examples/toggle_switch/LacI_producer'
        self.assertEqual(in_child_of, comp_ref.in_child_of)
        feature = 'https://sbolstandard.org/examples/LacI_producer/LacI_protein'
        self.assertEqual(feature, comp_ref.feature)


if __name__ == '__main__':
    unittest.main()
