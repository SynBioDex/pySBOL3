import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestImplementation(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        implementation = sbol3.Implementation('impl1')
        self.assertIsNotNone(implementation)
        self.assertIsNone(implementation.built)
        self.assertEqual(sbol3.SBOL_IMPLEMENTATION, implementation.type_uri)

    def test_create2(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1 = sbol3.Component('c1', [sbol3.SBO_DNA])
        implementation = sbol3.Implementation('impl1', built=c1)
        self.assertIsNotNone(implementation)
        self.assertEqual(c1.identity, implementation.built)
        self.assertEqual(sbol3.SBOL_IMPLEMENTATION, implementation.type_uri)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'entity', 'implementation',
                                 'implementation.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        search_uri = 'https://sbolstandard.org/examples/impl1'
        implementation = doc.find(search_uri)
        self.assertIsNotNone(implementation)
        self.assertIsInstance(implementation, sbol3.Implementation)
        tetr_uri = 'https://sbolstandard.org/examples/TetR_protein'
        built = tetr_uri
        self.assertCountEqual(built, implementation.built)


if __name__ == '__main__':
    unittest.main()
