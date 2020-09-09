import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestInterface(unittest.TestCase):

    def test_create(self):
        interface = sbol3.Interface('interface1')
        self.assertIsNotNone(interface)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'entity', 'interface',
                                 'interface.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        search_uri = 'https://sbolstandard.org/examples/LacI_producer/interface'
        interface = doc.find(search_uri)
        self.assertIsNotNone(interface)
        self.assertIsInstance(interface, sbol3.Interface)
        tetr_uri = 'https://sbolstandard.org/examples/LacI_producer/TetR_protein'
        laci_uri = 'https://sbolstandard.org/examples/LacI_producer/LacI_protein'
        atc_uri = 'https://sbolstandard.org/examples/LacI_producer/aTC'
        iface_input = [tetr_uri, laci_uri]
        self.assertCountEqual(iface_input, interface.input)
        output = [laci_uri]
        self.assertEqual(output, interface.output)
        non_directional = [atc_uri]
        self.assertEqual(non_directional, interface.non_directional)


if __name__ == '__main__':
    unittest.main()
