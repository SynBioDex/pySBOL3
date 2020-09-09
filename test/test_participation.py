import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestParticipation(unittest.TestCase):

    def test_create(self):
        identity = 'https://github.com/synbiodex/pysbol3/participation1'
        participant = 'https://github.com/synbiodex/pysbol3/participant1'
        p = sbol3.Participation(identity, [sbol3.SBO_INHIBITOR], participant)
        self.assertIsNotNone(p)
        self.assertEqual([sbol3.SBO_INHIBITOR], p.roles)
        self.assertEqual(participant, p.participant)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'toggle_switch',
                                 'toggle_switch.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        search_uri = ('https://sbolstandard.org/examples/'
                      'LacI_producer/interaction_2/participation_1')
        participation = doc.find(search_uri)
        self.assertIsNotNone(participation)
        self.assertIsInstance(participation, sbol3.Participation)
        participant = 'https://sbolstandard.org/examples/LacI_producer/subcomponent_5'
        self.assertEqual(participant, participation.participant)
        roles = [sbol3.SBO_TEMPLATE]
        self.assertEqual(roles, participation.roles)


if __name__ == '__main__':
    unittest.main()
