import os
import unittest

import sbol3

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestExternallyDefined(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_create(self):
        types = ['https://identifiers.org/SBO:0000247']
        definition = 'https://identifiers.org/CHEBI:3312'
        ext_def = sbol3.ExternallyDefined(types, definition)
        self.assertEqual(definition, ext_def.definition)
        self.assertCountEqual(types, ext_def.types)
        self.assertEqual(sbol3.SBOL_EXTERNALLY_DEFINED, ext_def.type_uri)

    def test_read_from_file(self):
        test_file = os.path.join(SBOL3_LOCATION, 'measurement_entity',
                                 'measurement', 'measurement.nt')
        doc = sbol3.Document()
        doc.read(test_file, sbol3.NTRIPLES)
        uri = 'https://sbolstandard.org/examples/M9_Glucose_CAA/CaCl2'
        ext_def = doc.find(uri)
        self.assertIsNotNone(ext_def)
        self.assertIsInstance(ext_def, sbol3.ExternallyDefined)
        self.assertCountEqual(['https://identifiers.org/SBO:0000247'], ext_def.types)
        self.assertEqual('https://identifiers.org/CHEBI:3312', ext_def.definition)
        self.assertEqual('CaCl2', ext_def.display_id)
        self.assertEqual(1, len(ext_def.measures))
        measure = ext_def.measures[0]
        measure_uri = 'https://sbolstandard.org/examples/M9_Glucose_CAA/CaCl2/measure1'
        self.assertEqual(measure_uri, measure.identity)
