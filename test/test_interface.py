import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestInterface(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        interface = sbol3.Interface()
        self.assertIsNotNone(interface)
        self.assertEqual(sbol3.SBOL_INTERFACE, interface.type_uri)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'entity', 'interface',
                                 'interface.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        search_uri = 'https://sbolstandard.org/examples/LacI_producer/Interface1'
        interface = doc.find(search_uri)
        self.assertIsNotNone(interface)
        self.assertIsInstance(interface, sbol3.Interface)
        tetr_uri = 'https://sbolstandard.org/examples/LacI_producer/SubComponent2'
        laci_uri = 'https://sbolstandard.org/examples/LacI_producer/SubComponent1'
        atc_uri = 'https://sbolstandard.org/examples/LacI_producer/SubComponent3'
        iface_input = [tetr_uri, laci_uri]
        self.assertCountEqual(iface_input, interface.inputs)
        output = [laci_uri]
        self.assertEqual(output, interface.outputs)
        nondirectional = [atc_uri]
        self.assertEqual(nondirectional, interface.nondirectionals)


if __name__ == '__main__':
    unittest.main()
