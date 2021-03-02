import unittest
from collections import Container

import sbol3


class TestComponent(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_roles(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c = sbol3.Component('c1', sbol3.SBO_DNA)
        self.assertListEqual([], list(c.roles))
        self.assertEqual([], c.roles)
        c.roles = [sbol3.SO_PROMOTER]
        # Make sure the underlying datatype did not get overwritten
        self.assertNotIsInstance(c.roles, list)
        self.assertIsInstance(c.roles, Container)
        self.assertIn(sbol3.SO_PROMOTER, c.roles)
        self.assertEqual([sbol3.SO_PROMOTER], c.roles)
        self.assertTrue(c.roles == [sbol3.SO_PROMOTER])
        self.assertTrue([sbol3.SO_PROMOTER] == c.roles)
        # Other list manipulations
        c.roles.append(sbol3.SO_CDS)
        self.assertEqual([sbol3.SO_PROMOTER, sbol3.SO_CDS], c.roles)
        self.assertEqual([sbol3.SO_CDS], c.roles[1:])
        c.roles[1:] = [sbol3.SO_RBS]
        self.assertEqual([sbol3.SO_PROMOTER, sbol3.SO_RBS], c.roles)
        self.assertEqual([sbol3.SO_RBS], c.roles[1:])

    def test_features(self):
        # See https://github.com/SynBioDex/pySBOL3/issues/149
        # Note: this example was modified when fixing
        #       https://github.com/SynBioDex/pySBOL3/issues/178
        #       media_variable is unused in the original example so
        #       it has been commented out here

        media_template = sbol3.LocalSubComponent(types=[sbol3.SBO_FUNCTIONAL_ENTITY])
        media_template.name = 'media template'

        # variable_uri = 'https://github.com/synbiodex/pysbol3/variable'
        # media_variable = sbol3.VariableFeature(cardinality=sbol3.SBOL_ONE,
        #                                        variable=media_template)
        # media_variable.variable = media_template

        all_sample_templates = [media_template]
        sample_template_uri = 'https://sd2e.org/measurement_template'
        sample_template = sbol3.Component(identity=sample_template_uri,
                                          types=sbol3.SBO_FUNCTIONAL_ENTITY)
        sample_template.name = 'measurement template'
        sample_template.features = all_sample_templates
        self.assertEqual(1, len(sample_template.features))
        self.assertEqual(media_template.identity,
                         sample_template.features[0].identity)

    def test_type_validation(self):
        # Test the validation of types on owned object properties by
        # going behind the scenes to set a bad value
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        c1 = sbol3.Component('c1', sbol3.SBO_DNA)
        report = c1.validate()
        self.assertEqual(0, len(report))
        c1._owned_objects[sbol3.SBOL_FEATURES] = [sbol3.Interface(),
                                                  sbol3.Implementation('i1')
                                                  ]
        report = c1.validate()
        # Expecting 2 errors, one for each inappropriate value
        self.assertEqual(2, len(report))


if __name__ == '__main__':
    unittest.main()
