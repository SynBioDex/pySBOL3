import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestParticipation(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        participant = 'https://github.com/synbiodex/pysbol3/participant1'
        p = sbol3.Participation([sbol3.SBO_INHIBITOR], participant)
        self.assertIsNotNone(p)
        self.assertEqual([sbol3.SBO_INHIBITOR], p.roles)
        self.assertEqual(participant, p.participant)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'toggle_switch',
                                 'toggle_switch.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        search_uri = ('https://sbolstandard.org/examples/'
                      'LacI_producer/Interaction2/Participation1')
        participation = doc.find(search_uri)
        self.assertIsNotNone(participation)
        self.assertIsInstance(participation, sbol3.Participation)
        participant = 'https://sbolstandard.org/examples/LacI_producer/SubComponent5'
        self.assertEqual(participant, participation.participant)
        roles = [sbol3.SBO_TEMPLATE]
        self.assertEqual(roles, participation.roles)

    def test_list_wrapping(self):
        # Ensure that at least certain properties handle automatic list
        # wrapping and are typed to do so.
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        test_role = sbol3.SBO_INHIBITOR
        participant_uri = 'https://example.org/participant'
        participation1 = sbol3.Participation(roles=test_role,
                                             participant=participant_uri)
        self.assertEqual([test_role], participation1.roles)


if __name__ == '__main__':
    unittest.main()
