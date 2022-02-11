import os
import posixpath
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
        uri = 'https://sbolstandard.org/examples/M9_Glucose_CAA/ExternallyDefined1'
        ext_def = doc.find(uri)
        self.assertIsNotNone(ext_def)
        self.assertIsInstance(ext_def, sbol3.ExternallyDefined)
        self.assertCountEqual(['https://identifiers.org/SBO:0000247'], ext_def.types)
        self.assertEqual('https://identifiers.org/CHEBI:3312', ext_def.definition)
        self.assertEqual('ExternallyDefined1', ext_def.display_id)
        self.assertEqual(1, len(ext_def.measures))
        measure = ext_def.measures[0]
        measure_uri = posixpath.join(uri, 'measure1')
        self.assertEqual(measure_uri, measure.identity)

    def test_list_wrapping(self):
        # Ensure that at least certain properties handle automatic list
        # wrapping and are typed to do so.
        # See https://github.com/SynBioDex/pySBOL3/issues/301
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        test_type = sbol3.SBO_DNA
        test_role = sbol3.SO_PROMOTER
        definition_uri = 'https://example.org/definition'
        ed1 = sbol3.ExternallyDefined(types=test_type,
                                      definition=definition_uri,
                                      roles=test_role)
        self.assertEqual([test_type], ed1.types)
        self.assertEqual([test_role], ed1.roles)


if __name__ == '__main__':
    unittest.main()
