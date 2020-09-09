import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestImplementation(unittest.TestCase):

    def test_create(self):
        implementation = sbol3.Implementation('impl1')
        self.assertIsNotNone(implementation)
        self.assertIsNone(implementation.built)

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
